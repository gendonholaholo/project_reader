import argparse
from pathlib import Path
import os
from openai import OpenAI, OpenAIError
from scanner.file_scanner import FileScanner
from analyzer.project_analyzer import ProjectAnalyzer
from describer.llm_describer import LLMDescriber
from writer.output_writer import OutputWriter
import config

def check_api_key():
    """Check if OpenAI API key is set."""
    if not config.OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it using:")
        print("  export OPENAI_API_KEY='your-api-key-here'  # On Linux/Mac")
        print("  set OPENAI_API_KEY=your-api-key-here  # On Windows")
        return False
    print(f"Using API key: {config.OPENAI_API_KEY[:10]}...")  # Only show first 10 chars for security
    print(f"Using base URL: {config.OPENAI_API_BASE}")
    print(f"Using model: {config.OPENAI_MODEL}")
    return True

def handle_openai_error(e: OpenAIError) -> str:
    """Handle OpenAI API errors with user-friendly messages."""
    if "insufficient_quota" in str(e):
        return """
Error: OpenAI API quota exceeded.
Please check your OpenAI account billing and quota at: https://platform.openai.com/account/billing
Common solutions:
1. Add a payment method to your OpenAI account
2. Wait for your quota to reset
3. Upgrade your OpenAI account plan
"""
    elif "model_not_found" in str(e):
        return f"""
Error: The model '{config.OPENAI_MODEL}' is not available.
Please modify config.py to use a model you have access to, such as:
- gpt-3.5-turbo (recommended)
- gpt-3.5-turbo-16k (for longer texts)
"""
    elif "invalid_api_key" in str(e):
        return """
Error: Invalid OpenAI API key.
Please check that your API key is correct and properly set in the environment variable.
"""
    else:
        return f"OpenAI API error: {str(e)}"

def main():
    # Check OpenAI API key first
    if not check_api_key():
        return

    print("Debug: Starting main function")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze a Python project and generate documentation.')
    parser.add_argument('--folder', type=str, required=True, help='Path to the project folder to analyze')
    parser.add_argument('--output', type=str, help='Path to the output file (default: project_analysis.txt)')
    args = parser.parse_args()

    print(f"Debug: Analyzing folder: {args.folder}")
    
    # Validate input folder
    project_path = Path(args.folder)
    if not project_path.exists() or not project_path.is_dir():
        print(f"Error: {args.folder} is not a valid directory")
        return

    try:
        print("Debug: Initializing components")
        # Initialize components
        file_scanner = FileScanner(project_path)
        project_analyzer = ProjectAnalyzer(file_scanner)
        llm_describer = LLMDescriber()
        output_writer = OutputWriter(args.output)

        # Scan and analyze the project
        print("Debug: Starting file scan")
        files, directories = file_scanner.scan()
        print(f"Debug: Found {len(files['python'])} Python files")
        
        print("Debug: Starting project analysis")
        try:
            analysis_results = project_analyzer.analyze_project()
            print("Debug: Project analysis completed")
        except OpenAIError as e:
            print("Debug: OpenAI error during project analysis:")
            print(handle_openai_error(e))
            return
        except Exception as e:
            print(f"Debug: Unexpected error during project analysis: {str(e)}")
            raise
        
        print("Generating project description...")
        try:
            description = llm_describer.describe_project(analysis_results)
        except OpenAIError as e:
            print(handle_openai_error(e))
            return
        
        print("Writing analysis results...")
        output_writer.write_analysis(analysis_results, description)
        
        # Generate and write module descriptions
        print("Generating module descriptions...")
        for file in files['python']:
            try:
                content = file_scanner.get_file_content(file)
                module_description = llm_describer.describe_module(file, content)
                output_writer.write_module_description(file, module_description)
            except OpenAIError as e:
                print(f"\nError analyzing {file.name}:")
                print(handle_openai_error(e))
                continue
        
        # Generate and write directory descriptions
        print("Generating directory descriptions...")
        for directory in directories:
            dir_contents = [f for f in files['python'] if f.parent == directory]
            if dir_contents:
                try:
                    dir_description = llm_describer.describe_directory(directory, dir_contents)
                    output_writer.write_directory_description(directory, dir_description)
                except OpenAIError as e:
                    print(f"\nError analyzing directory {directory.name}:")
                    print(handle_openai_error(e))
                    continue
        
        print(f"\nAnalysis complete! Results written to {output_writer.output_path}")
        
    except Exception as e:
        if isinstance(e, OpenAIError):
            print(handle_openai_error(e))
        else:
            print(f"Error during analysis: {str(e)}")
        return

if __name__ == "__main__":
    main() 