import os
from typing import Dict, List, Set, Tuple
from pathlib import Path
import config

class FileScanner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        self.files: Dict[str, List[Path]] = {
            "python": [],
            "documentation": [],
            "config": [],
            "other": []
        }
        self.directories: Set[Path] = set()

    def scan(self) -> Tuple[Dict[str, List[Path]], Set[Path]]:
        for root, dirs, files in os.walk(self.project_path):
            root_path = Path(root)
            dirs[:] = [d for d in dirs if d not in config.IGNORED_DIRECTORIES]
            self.directories.add(root_path)
            for file in files:
                if file in config.IGNORED_FILES:
                    continue
                file_path = root_path / file
                ext = file_path.suffix.lower()
                if ext in config.PYTHON_EXTENSIONS:
                    self.files["python"].append(file_path)
                elif ext in config.DOCUMENTATION_EXTENSIONS:
                    self.files["documentation"].append(file_path)
                elif ext in config.CONFIG_EXTENSIONS:
                    self.files["config"].append(file_path)
                else:
                    self.files["other"].append(file_path)
        return self.files, self.directories

    def get_file_content(self, file_path: Path) -> str:
        try:
            if file_path.stat().st_size > config.MAX_FILE_SIZE:
                return f"[File too large to analyze: {file_path.stat().st_size} bytes]"
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {str(e)}]"

    def get_project_structure(self) -> str:
        structure = []
        for directory in sorted(self.directories):
            rel_path = directory.relative_to(self.project_path)
            if str(rel_path) == '.':
                continue
            indent = '  ' * (len(rel_path.parts) - 1)
            structure.append(f"{indent}- {rel_path.name}/")
            for file_type, files in self.files.items():
                for file in files:
                    if file.parent == directory:
                        structure.append(f"{indent}  - {file.name}")
        return "\n".join(structure) 