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
        # Initial setup
        log.debug("Setting up directories...")
        bee_dir = "test_data/bee"
        limitless_dir = "test_data/limitless"
        output_dir = "output"
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        log.debug(f"Output directory ensured: {output_dir}")
        
        # Directory check with detailed logging
        for dir_path in [bee_dir, limitless_dir]:
            log.debug(f"Checking directory: {dir_path}")
            if not os.path.exists(dir_path):
                log.error(f"Directory not found: {dir_path}")
                return
            log.debug(f"Directory contents for {dir_path}: {os.listdir(dir_path)}")

        # Parser phase
        log.debug("=== Starting Parser Phase ===")
        parser = MarkdownParser(bee_dir, limitless_dir)
        parsed_data = parser.get_parsed_data()
        log.debug(f"Parser returned data with keys: {parsed_data.keys()}")
        
        # Summarizer phase
        log.debug("=== Starting Summarizer Phase ===")
        openai_api_key = get_openai_api_key()
        log.debug("Got API key")
        
        summarizer = AIEnhancedSummarizer(parsed_data, openai_api_key)
        log.debug("Created summarizer")
        
        # Summarizer phase debug
        summaries = summarizer.generate_summary()
        log.debug("=== Summarizer Output Debug ===")
        log.debug(f"Raw summaries output: {summaries}")  # Add full output logging
        log.debug(f"Type: {type(summaries)}")
        log.debug(f"Dir: {dir(summaries)}")  # Show available methods/attributes
        
        # Pre-resolver detailed inspection
        log.debug("=== Pre-Resolver Detailed Inspection ===")
        if isinstance(summaries, str):
            log.error("Summarizer returned a string instead of expected dictionary")
            log.debug(f"String content (first 500 chars): {summaries[:500]}")
        elif isinstance(summaries, dict):
            log.debug(f"Dictionary keys: {list(summaries.keys())}")
            for k, v in summaries.items():
                log.debug(f"Key '{k}' contains type: {type(v)}")
                log.debug(f"Value preview: {str(v)[:200]}")
        else:
            log.error(f"Unexpected type returned: {type(summaries)}")
        
        # Continue with existing resolver code...
        log.debug("=== Starting Resolver Phase ===")
        bee_data = summaries.get("bee", {})
        limitless_data = summaries.get("limitless", {})
        log.debug(f"Bee data type: {type(bee_data)}")
        log.debug(f"Limitless data type: {type(limitless_data)}")
        
        resolver = AIEnhancedResolver(bee_data, limitless_data)
        resolved_summaries = resolver.resolve()
        log.debug(f"Resolved summaries type: {type(resolved_summaries)}")
        
        # Generator phase
        log.debug("=== Starting Generator Phase ===")
        generator = SummaryGenerator(resolved_summaries, output_dir)
        generator.generate()
        log.debug("Summary generation complete")
        
        # Verify output
        if os.path.exists(output_dir):
            output_files = os.listdir(output_dir)
            log.debug(f"Output directory contents: {output_files}")
        
    except Exception as e:
        log.error(f"Exception in process_summaries: {str(e)}\n{traceback.format_exc()}")
        raise
    finally:
        log.debug("=== Exiting process_summaries() ===")
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
