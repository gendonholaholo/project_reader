from openai import OpenAI, OpenAIError
import config
from typing import Dict, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class LLMDescriber:
    def __init__(self):
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
            raise # Re-raise the exception to be caught in main

    def _call_groq_api(self, prompt: str) -> str:
        try:
            logger.debug(f"Sending prompt to Groq: {prompt[:100]}...")
            response = self.client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            logger.debug(f"Received response from Groq: {content[:100]}...")
            return content
        except OpenAIError as e:
            logger.error(f"Groq API error during description call: {e}")
            raise # Re-raise the specific OpenAIError
        except Exception as e:
            logger.exception("Unexpected error during Groq API call")
            raise # Re-raise other exceptions

    def describe_project(self, analysis_results: Dict[str, str]) -> str:
        logger.debug("Describing project...")
        prompt = f"""
        Berdasarkan analisis proyek berikut, tulis deskripsi yang komprehensif dan profesional dalam bahasa Indonesia:
        
        Nama Proyek: {analysis_results['project_name']}
        Tujuan: {analysis_results['project_purpose']}
        Teknologi: {analysis_results['technologies']}
        Analisis: {analysis_results['project_analysis']}
        Catatan Tambahan: {analysis_results['additional_notes']}
        
        Tulis deskripsi profesional yang terstruktur dengan baik yang:
        1. Dimulai dengan pengantar yang jelas
        2. Menjelaskan tujuan dan sasaran proyek
        3. Menjelaskan arsitektur teknis dan pilihan
        4. Menyoroti fitur dan komponen utama
        5. Menyimpulkan dengan pertimbangan penting
        
        Gunakan bahasa profesional dan pertahankan nada yang teknis namun mudah dipahami.
        """
        return self._call_groq_api(prompt)

    def describe_module(self, module_path: Path, content: str) -> str:
        logger.debug(f"Describing module: {module_path.name}")
        prompt = f"""
        Analisis modul Python berikut dan berikan deskripsi yang jelas dalam bahasa Indonesia:
        
        Modul: {module_path.name}
        Isi:
        {content[:config.MAX_TOKENS_PER_FILE]}
        
        Berikan deskripsi yang:
        1. Menjelaskan tujuan modul
        2. Mendeskripsikan komponen dan fungsi utamanya
        3. Menyoroti pola atau pilihan desain penting
        4. Mencatat ketergantungan atau hubungan dengan modul lain
        
        Pertahankan deskripsi yang ringkas dan profesional.
        """
        return self._call_groq_api(prompt)

    def describe_directory(self, dir_path: Path, contents: List[Path]) -> str:
        logger.debug(f"Describing directory: {dir_path.name}")
        prompt = f"""
        Analisis direktori berikut dan isinya dalam bahasa Indonesia:
        
        Direktori: {dir_path.name}
        Isi: {[f.name for f in contents]}
        
        Berikan deskripsi yang:
        1. Menjelaskan peran direktori dalam proyek
        2. Mendeskripsikan bagaimana isinya diorganisir
        3. Menjelaskan pola atau konvensi yang digunakan
        4. Mencatat hubungan penting dengan direktori lain
        
        Pertahankan deskripsi yang ringkas dan profesional.
        """
        return self._call_groq_api(prompt) 