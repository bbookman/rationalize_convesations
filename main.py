import os
from processing.parser import MarkdownParser
from processing.summarizer import AIEnhancedSummarizer
from processing.resolver import AIEnhancedResolver
from processing.generator import SummaryGenerator
import json
from utils.logger import log
import traceback
import sys


# Retrieve OpenAI API key from environment
def get_openai_api_key():
    
    """Retrieve OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is missing! Set OPENAI_API_KEY in your environment.")
    return api_key

def process_summaries():
    log.debug("=== Entering process_summaries() ===")
    try:
        log.debug("First line of process_summaries")
        # Force an early log flush
        sys.stdout.flush()
        sys.stderr.flush()
        
        log.debug("Setting up directories...")
        bee_dir = "test_data/bee"
        limitless_dir = "test_data/limitless"
        output_dir = "output"
        
        # Directory check with detailed logging
        for dir_path in [bee_dir, limitless_dir]:
            log.debug(f"Checking directory: {dir_path}")
            if not os.path.exists(dir_path):
                log.error(f"Directory not found: {dir_path}")
                log.debug("=== Exiting process_summaries() due to missing directory ===")
                return

        # Continue only if directories exist
        log.debug("All directories present, continuing...")
        
        log.debug("Creating parser...")
        parser = MarkdownParser(bee_dir, limitless_dir)
        parsed_data = parser.get_parsed_data()

        # Debug logging before summarizer creation
        log.debug(f"Creating summarizer with:")
        log.debug(f"parsed_data type: {type(parsed_data)}")
        log.debug(f"parsed_data keys: {list(parsed_data.keys() if isinstance(parsed_data, dict) else [])}")
        log.debug(f"API key present: {bool(get_openai_api_key())}")

        # Create summarizer with try-except for initialization
        try:
            summarizer = AIEnhancedSummarizer(parsed_data, get_openai_api_key())
            log.debug("Summarizer created successfully")
        except Exception as e:
            log.error(f"Failed to create summarizer: {e}")
            raise

        # Debug logging before and after summary generation
        try:
            log.debug("Starting summary generation...")
            summaries = summarizer.generate_summary()
            log.debug("Summary generation complete")
        except Exception as e:
            log.error(f"Failed during summary generation: {e}")
            raise

    except Exception as e:
        log.error(f"Exception in process_summaries: {str(e)}\n{traceback.format_exc()}")
        raise
    finally:
        log.debug("=== Exiting process_summaries() ===")
        # Force final log flush
        sys.stdout.flush()
        sys.stderr.flush()

if __name__ == "__main__":
    log.info("Application starting...")
    try:
        log.debug("About to call process_summaries()")
        process_summaries()
        log.debug("Finished process_summaries()")
    except Exception as e:
        log.error(f"Main execution failed: {e}\n{traceback.format_exc()}")
        sys.exit(1)
    finally:
        log.info("Application ending...")
        sys.stdout.flush()
        sys.stderr.flush()
