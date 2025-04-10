import os
from processing.parser import MarkdownParser
from processing.summarizer import AIEnhancedSummarizer
from processing.resolver import AIEnhancedResolver
from processing.generator import SummaryGenerator
import json


# Retrieve OpenAI API key from environment
def get_openai_api_key():
    
    """Retrieve OpenAI API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is missing! Set OPENAI_API_KEY in your environment.")
    return api_key

def process_summaries():
    
    """Main workflow for parsing markdown files, summarizing, resolving conflicts, and generating output."""
    openai_api_key = get_openai_api_key()
    

    try:
        # Define directory paths directly
        bee_dir = "test_data/bee"
        limitless_dir = "test_data/limitless"
        output_dir = "output"

        # Initialize parser
        parser = MarkdownParser(bee_dir, limitless_dir)
        parsed_data = parser.get_parsed_data()

        # Generate AI-enhanced summaries
        summarizer = AIEnhancedSummarizer(parsed_data, openai_api_key)
        summaries = summarizer.generate_summary()

        # Resolve conflicts between Bee & Limitless data
        resolver = AIEnhancedResolver(summaries.get("bee", {}), summaries.get("limitless", {}))
        refined_summaries = resolver.resolve_conflicts()
        print("Type of refined_summaries:", type(refined_summaries))

        # Format and save final summaries
        print("Type of refined_summaries:", type(refined_summaries))
        print(json.dumps(refined_summaries, indent=2))  # Pretty-print structure

        generator = SummaryGenerator(refined_summaries, output_dir)
        # print("Resolved Summaries Structure:", type(refined_summaries))
        # print(refined_summaries)


        generator.generate_summaries()

        print("Processing complete. Summaries saved in the output directory.")

    except Exception as e:

        print(f"Error encountered: {e}")

if __name__ == "__main__":
    process_summaries()
