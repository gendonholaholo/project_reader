import argparse
from pathlib import Path
import os
from openai import OpenAI, OpenAIError
from scanner.file_scanner import FileScanner
from analyzer.project_analyzer import ProjectAnalyzer
from describer.llm_describer import LLMDescriber
from writer.output_writer import OutputWriter
import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_api_key():
    """Check if Groq API key is set."""
    if not config.GROQ_API_KEY:
        logger.error("GROQ_API_KEY environment variable is not set.")
        logger.error("Please set it using:")
        logger.error("  export GROQ_API_KEY='your-api-key-here'  # On Linux/Mac")
        logger.error("  set GROQ_API_KEY=your-api-key-here  # On Windows")
        return False
    logger.info(f"Using API key: {config.GROQ_API_KEY[:10]}...")
    logger.info(f"Using base URL: {config.GROQ_API_BASE}")
    logger.info(f"Using model: {config.GROQ_MODEL}")
    return True

def handle_groq_error(e: OpenAIError) -> str:
    """Handle Groq API errors with user-friendly messages."""
    error_message = f"Groq API error: {e}"
    try:
        # Try to get structured error details if available
        error_data = e.response.json().get('error', {})
        code = error_data.get('code')
        message = error_data.get('message', str(e)) # Fallback to default message

        if code == 'rate_limit_exceeded':
            error_message = f"""
Error: Groq API rate limit exceeded.
Message: {message}
Please check your Groq account billing and quota at: https://console.groq.com/settings/billing
"""
        elif code == 'model_not_found' or 'decommissioned' in message:
             error_message = f"""
Error: The model '{config.GROQ_MODEL}' is not available or decommissioned.
Message: {message}
Please check available models or modify config.py.
"""
        elif code == 'invalid_api_key' or e.http_status == 401:
             error_message = f"""
Error: Invalid Groq API key.
Message: {message}
Please check that your API key is correct and properly set in the environment variable.
"""
        else:
             error_message = f"Groq API error (Code: {code}): {message}"

    except Exception:
        # Fallback if parsing error details fails
        logger.debug("Could not parse structured error details from Groq API response.", exc_info=True)
        # Use basic string checks as fallback
        if "insufficient_quota" in str(e) or "rate_limit_exceeded" in str(e):
            error_message = "Error: Groq API quota exceeded or rate limit reached."
        elif "model_not_found" in str(e) or "decommissioned" in str(e):
            error_message = f"Error: The model '{config.GROQ_MODEL}' is not available or decommissioned."
        elif "invalid_api_key" in str(e) or getattr(e, 'http_status', None) == 401:
            error_message = "Error: Invalid Groq API key."

    return error_message

def main():
    # Check Groq API key first
    if not check_api_key():
        return

    logger.info("Starting main function")

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze a Python project and generate documentation.')
    parser.add_argument('--folder', type=str, required=True, help='Path to the project folder to analyze')
    parser.add_argument('--output', type=str, help='Path to the output file (default: project_analysis.txt)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    # Set logging level based on debug flag
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled.")

    logger.info(f"Analyzing folder: {args.folder}")

    # Validate input folder
    project_path = Path(args.folder)
    if not project_path.exists() or not project_path.is_dir():
        logger.error(f"{args.folder} is not a valid directory")
        return

    try:
        logger.info("Initializing components")
        # Initialize components
        file_scanner = FileScanner(project_path)
        project_analyzer = ProjectAnalyzer(file_scanner)
        llm_describer = LLMDescriber()
        output_writer = OutputWriter(args.output)

        # Scan and analyze the project
        logger.info("Starting file scan")
        files, directories = file_scanner.scan()
        logger.info(f"Found {len(files['python'])} Python files")

        logger.info("Starting project analysis")
        try:
            analysis_results = project_analyzer.analyze_project()
            logger.info("Project analysis completed")
        except OpenAIError as e:
            logger.error("Groq error during project analysis:")
            logger.error(handle_groq_error(e))
            return
        except Exception as e:
            logger.exception("Unexpected error during project analysis") # Logs traceback
            return # Exit on unexpected analysis error

        logger.info("Generating project description...")
        try:
            description = llm_describer.describe_project(analysis_results)
        except OpenAIError as e:
            logger.error("Groq error during project description generation:")
            logger.error(handle_groq_error(e))
            description = "Error: Could not generate project description due to API error." # Provide fallback
        except Exception as e:
             logger.exception("Unexpected error during project description generation")
             description = "Error: Could not generate project description due to unexpected error."

        logger.info("Writing analysis results...")
        output_writer.write_analysis(analysis_results, description)

        # Generate and write module descriptions
        logger.info("Generating module descriptions...")
        for file in files['python']:
            logger.debug(f"Analyzing module: {file.name}")
            try:
                content = file_scanner.get_file_content(file)
                module_description = llm_describer.describe_module(file, content)
                output_writer.write_module_description(file, module_description)
            except OpenAIError as e:
                logger.error(f"Error analyzing module {file.name}:")
                logger.error(handle_groq_error(e))
                # Continue with the next module
            except Exception as e:
                logger.exception(f"Unexpected error analyzing module {file.name}")
                # Continue with the next module

        # Generate and write directory descriptions
        logger.info("Generating directory descriptions...")
        for directory in directories:
             # Ensure directory is not in ignored list before processing
            if directory.name in config.IGNORED_DIRECTORIES or directory == project_path:
                 continue
            logger.debug(f"Analyzing directory: {directory.name}")
            dir_contents = [f for f in files['python'] if f.parent == directory]
            if dir_contents:
                try:
                    dir_description = llm_describer.describe_directory(directory, dir_contents)
                    output_writer.write_directory_description(directory, dir_description)
                except OpenAIError as e:
                    logger.error(f"Error analyzing directory {directory.name}:")
                    logger.error(handle_groq_error(e))
                    # Continue with the next directory
                except Exception as e:
                    logger.exception(f"Unexpected error analyzing directory {directory.name}")
                    # Continue with the next directory

        logger.info(f"Analysis complete! Results written to {output_writer.output_path}")

    except Exception as e:
        # Catch-all for initialization or other unexpected errors
        logger.exception("An unexpected error occurred during the process") # Use logger.exception to include traceback

if __name__ == "__main__":
    main() 