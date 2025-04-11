import os
from typing import Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# OpenAI API Configuration
OPENAI_API_KEY = "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"  # Groq API key
OPENAI_MODEL = "llama-3.3-70b-versatile"  # Using Groq's LLaMA model
OPENAI_API_BASE = "https://api.groq.com/openai/v1"  # Groq API endpoint

# Analysis Configuration
DEFAULT_OUTPUT_FILE = "project_analysis.txt"
IGNORED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    ".idea",
    ".vscode"
}

IGNORED_FILES = {
    ".gitignore",
    ".env",
    ".DS_Store"
}

# File extensions to analyze
PYTHON_EXTENSIONS = {".py"}
DOCUMENTATION_EXTENSIONS = {".md", ".txt", ".rst"}
CONFIG_EXTENSIONS = {".toml", ".yaml", ".yml", ".json"}

# Analysis settings
MAX_FILE_SIZE = 1024 * 1024  # 1MB
MAX_TOKENS_PER_FILE = 2000

# Output Configuration
DEFAULT_OUTPUT_DIR = "output"

# Output formatting
OUTPUT_TEMPLATE = """
📁 Proyek: {project_name}
🎯 Tujuan: {project_purpose}

📂 Struktur:
{project_structure}

🔍 Analisis:
{project_analysis}

🛠️ Teknologi:
{technologies}

📝 Catatan Tambahan:
{additional_notes}
""" 