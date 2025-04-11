from typing import Dict
from pathlib import Path
import config
from datetime import datetime
import os

class OutputWriter:
    def __init__(self, output_path: str = None):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_dir = Path("output") / f"analisis-{timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.output_path = self.output_dir / "analisis_proyek.txt"

    def write_analysis(self, analysis_results: Dict[str, str], description: str) -> None:
        output = config.OUTPUT_TEMPLATE.format(
            project_name=analysis_results['project_name'],
            project_purpose=analysis_results['project_purpose'],
            project_structure=analysis_results.get('project_structure', ''),
            project_analysis=analysis_results['project_analysis'],
            technologies=analysis_results['technologies'],
            additional_notes=analysis_results['additional_notes']
        )

        metadata = f"""
Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model Analisis: {config.OPENAI_MODEL}
"""
        output = metadata + output

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(output)

    def write_module_description(self, module_path: Path, description: str) -> None:
        modules_dir = self.output_dir / "modul"
        modules_dir.mkdir(exist_ok=True)
        
        output = f"""
Modul: {module_path.name}
Path: {module_path}

Deskripsi:
{description}

Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        output_path = modules_dir / f"{module_path.stem}_deskripsi.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)

    def write_directory_description(self, dir_path: Path, description: str) -> None:
        dirs_dir = self.output_dir / "direktori"
        dirs_dir.mkdir(exist_ok=True)
        
        output = f"""
Direktori: {dir_path.name}
Path: {dir_path}

Deskripsi:
{description}

Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        output_path = dirs_dir / f"{dir_path.name}_deskripsi.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output) 