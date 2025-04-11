# Project Analyzer

A Python application that analyzes project structures and generates comprehensive documentation using AI.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/gendonholaholo/project_reader)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features

- Scans and analyzes Python project structures
- Identifies project purpose and technologies
- Generates professional documentation
- Creates detailed module and directory descriptions
- Uses OpenAI's GPT models for natural language analysis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gendonholaholo/project_reader.git
cd project_reader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
or using setup.py:
```bash
pip install .
```

3. Set up your OpenAI API key:
```bash
# On Linux/Mac
export OPENAI_API_KEY='your-api-key-here'

# On Windows
set OPENAI_API_KEY=your-api-key-here
```
Alternatively, you can create a `.env` file in the project root with:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the analyzer on a project folder:

```bash
python main.py --folder ./path-to-project --output ./analysis.txt
```

Arguments:
- `--folder`: Path to the project folder to analyze (required)
- `--output`: Path to the output file (optional, defaults to project_analysis.txt)

## Project Structure

```
project-analyzer/
├── scanner/            # File scanning module
│   └── file_scanner.py
├── analyzer/           # Project analysis module
│   └── project_analyzer.py
├── describer/          # LLM description module
│   └── llm_describer.py
├── writer/             # Output writing module
│   └── output_writer.py
├── output/             # Generated analysis output directory
├── main.py             # Entry point
├── config.py           # Configuration
├── setup.py            # Package installation script
├── requirements.txt    # Dependencies
├── .env                # Environment variables (optional)
└── README.md           # Documentation
```

## Output Format

The analyzer generates:
1. A main analysis file with project overview
2. Individual module descriptions
3. Directory structure descriptions

Example output:
```txt
Project: example-project
Purpose: RESTful API service

Structure:
- core/
  - api.py
  - models.py
- utils/
  - helpers.py
  - validators.py

Analysis:
Project follows a clean architecture pattern...
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- GitHub: [@gendonholaholo](https://github.com/gendonholaholo)
- Repository: [project_reader](https://github.com/gendonholaholo/project_reader) 
___
~Mas Gendon
