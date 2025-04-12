from typing import Dict, List, Set, Tuple
from pathlib import Path
from openai import OpenAI, OpenAIError
import config
from scanner.file_scanner import FileScanner
import logging

logger = logging.getLogger(__name__)

class ProjectAnalyzer:
    def __init__(self, file_scanner: FileScanner):
        self.file_scanner = file_scanner
        self.project_path = file_scanner.project_path
        self.project_name = file_scanner.project_name
        try:
            self.client = OpenAI(
                api_key=config.GROQ_API_KEY,
                base_url=config.GROQ_API_BASE,
                default_headers={
                    "Content-Type": "application/json"
                }
            )
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}", exc_info=True)
            raise  # Re-raise the exception to be caught in main

    def _call_groq_api(self, prompt: str) -> str:
        try:
            logger.debug(f"Sending prompt to Groq: {prompt[:100]}...") # Log snippet of prompt
            response = self.client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            logger.debug(f"Received response from Groq: {content[:100]}...")
            return content
        except OpenAIError as e:
            logger.error(f"Groq API error during analysis call: {e}")
            raise # Re-raise the specific OpenAIError to be handled in main
        except Exception as e:
            logger.exception("Unexpected error during Groq API call")
            raise # Re-raise other exceptions

    def analyze_project(self) -> Dict[str, str]:
        logger.info("Scanning project files...")
        files, directories = self.file_scanner.scan()
        logger.info("Analyzing project components...")
        project_purpose = self._analyze_project_purpose(files["documentation"])
        technologies = self._analyze_technologies(files["python"])
        project_analysis = self._analyze_project_structure(directories, files)
        additional_notes = self._generate_additional_notes(files)
        logger.info("Project analysis components generated.")
        return {
            "project_name": self.project_name,
            "project_purpose": project_purpose,
            "technologies": technologies,
            "project_analysis": project_analysis,
            "additional_notes": additional_notes
        }

    def _analyze_project_purpose(self, doc_files: List[Path]) -> str:
        logger.debug("Analyzing project purpose...")
        if not doc_files:
            logger.warning("No documentation files found to determine project purpose.")
            return "No documentation found to determine project purpose."
        content = ""
        for file in doc_files:
            content += self.file_scanner.get_file_content(file)
        prompt = f"""
        Analisis dokumentasi proyek berikut dan tentukan tujuan utamanya:
        {content[:config.MAX_TOKENS_PER_FILE]}
        
        Berikan deskripsi singkat dan profesional tentang tujuan proyek dalam bahasa Indonesia.
        """
        return self._call_groq_api(prompt)

    def _analyze_technologies(self, python_files: List[Path]) -> str:
        logger.debug("Analyzing technologies...")
        if not python_files:
            logger.warning("No Python files found to analyze technologies.")
            return "No Python files found to analyze technologies."
        content = ""
        files_to_analyze = python_files[:5] # Limit analysis to first 5 files for performance
        logger.debug(f"Analyzing technologies from files: {[f.name for f in files_to_analyze]}")
        for file in files_to_analyze:
            content += f"\n\nFile: {file.name}\n"
            content += self.file_scanner.get_file_content(file)
        prompt = f"""
        Analisis kode Python berikut dan identifikasi:
        1. Teknologi dan library utama yang digunakan
        2. Framework yang digunakan (jika ada)
        3. Pola arsitektur kunci
        
        Kode:
        {content[:config.MAX_TOKENS_PER_FILE]}
        
        Berikan daftar singkat teknologi dan pola yang ditemukan dalam bahasa Indonesia.
        """
        return self._call_groq_api(prompt)

    def _analyze_project_structure(self, directories: Set[Path], files: Dict[str, List[Path]]) -> str:
        logger.debug("Analyzing project structure...")
        structure = self.file_scanner.get_project_structure()
        prompt = f"""
        Analisis struktur proyek berikut dan berikan wawasan tentang:
        1. Arsitektur keseluruhan
        2. Organisasi modul
        3. Pola umum dalam struktur direktori
        
        Struktur:
        {structure}
        
        Berikan analisis profesional tentang struktur proyek dalam bahasa Indonesia.
        """
        return self._call_groq_api(prompt)

    def _generate_additional_notes(self, files: Dict[str, List[Path]]) -> str:
        logger.debug("Generating additional notes...")
        prompt = f"""
        Berdasarkan informasi proyek berikut, berikan wawasan tambahan:
        - File Python: {len(files['python'])}
        - File dokumentasi: {len(files['documentation'])}
        - File konfigurasi: {len(files['config'])}
        - File lainnya: {len(files['other'])}
        
        Berikan observasi atau rekomendasi tambahan tentang proyek dalam bahasa Indonesia.
        """
        return self._call_groq_api(prompt) 