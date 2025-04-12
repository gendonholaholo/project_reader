import os
from typing import Dict, Any
from dotenv import dotenv_values
from pathlib import Path

# Load environment variables from .env file
env_path = Path.cwd() / '.env'
print(f"Loading .env from: {env_path}")

env_values = dotenv_values(env_path)
GROQ_API_KEY = env_values.get('GROQ_API_KEY')
GROQ_MODEL = env_values.get('GROQ_MODEL', 'deepseek-r1-distill-llama-70b')
GROQ_API_BASE = env_values.get('GROQ_API_BASE', 'https://api.groq.com/openai/v1/chat/completions')

print(f"\nAPI Key loaded: {GROQ_API_KEY[:10]}..." if GROQ_API_KEY else "No API Key loaded!")
print(f"Model loaded: {GROQ_MODEL}")
print(f"API Base loaded: {GROQ_API_BASE}")

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
