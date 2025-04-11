from openai import OpenAI
import config
from typing import Dict, List
from pathlib import Path

class LLMDescriber:
    def __init__(self):
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_API_BASE,
            default_headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config.OPENAI_API_KEY}"
            }
        )

    def describe_project(self, analysis_results: Dict[str, str]) -> str:
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
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def describe_module(self, module_path: Path, content: str) -> str:
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
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def describe_directory(self, dir_path: Path, contents: List[Path]) -> str:
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
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip() 