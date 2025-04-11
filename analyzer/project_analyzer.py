from typing import Dict, List, Set, Tuple
from pathlib import Path
from openai import OpenAI
import config
from scanner.file_scanner import FileScanner

class ProjectAnalyzer:
    def __init__(self, file_scanner: FileScanner):
        self.file_scanner = file_scanner
        self.project_path = file_scanner.project_path
        self.project_name = file_scanner.project_name
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_API_BASE,
            default_headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.OPENAI_API_KEY}"
            }
        )

    def analyze_project(self) -> Dict[str, str]:
        files, directories = self.file_scanner.scan()
        project_purpose = self._analyze_project_purpose(files["documentation"])
        technologies = self._analyze_technologies(files["python"])
        project_analysis = self._analyze_project_structure(directories, files)
        return {
            "project_name": self.project_name,
            "project_purpose": project_purpose,
            "technologies": technologies,
            "project_analysis": project_analysis,
            "additional_notes": self._generate_additional_notes(files)
        }

    def _analyze_project_purpose(self, doc_files: List[Path]) -> str:
        if not doc_files:
            return "No documentation found to determine project purpose."
        content = ""
        for file in doc_files:
            content += self.file_scanner.get_file_content(file)
        prompt = f"""
        Analisis dokumentasi proyek berikut dan tentukan tujuan utamanya:
        {content[:config.MAX_TOKENS_PER_FILE]}
        
        Berikan deskripsi singkat dan profesional tentang tujuan proyek dalam bahasa Indonesia.
        """
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def _analyze_technologies(self, python_files: List[Path]) -> str:
        if not python_files:
            return "No Python files found to analyze technologies."
        content = ""
        for file in python_files[:5]:
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
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def _analyze_project_structure(self, directories: Set[Path], files: Dict[str, List[Path]]) -> str:
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
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def _generate_additional_notes(self, files: Dict[str, List[Path]]) -> str:
        prompt = f"""
        Berdasarkan informasi proyek berikut, berikan wawasan tambahan:
        - File Python: {len(files['python'])}
        - File dokumentasi: {len(files['documentation'])}
        - File konfigurasi: {len(files['config'])}
        - File lainnya: {len(files['other'])}
        
        Berikan observasi atau rekomendasi tambahan tentang proyek dalam bahasa Indonesia.
        """
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip() 