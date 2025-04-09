import os
import traceback
from openai import OpenAI
from utils.logger import log


class AIEnhancedSummarizer:
    def __init__(self, parsed_data, api_key=None):
        """Initialize summarizer with parsed markdown data."""
        self.parsed_data = parsed_data
        self.api_key = os.getenv("OPENAI_API_KEY")  # Retrieve API key from environment
        

        if not self.api_key:
            raise ValueError("OpenAI API key is missing! Set OPENAI_API_KEY in your environment.")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def call_openai(self, prompt):
        log.debug("Calling OpenAI")
        """Send a request to GPT-4o Mini for enhanced summarization with error handling."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI tasked with generating refined summaries from parsed markdown data."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None  # Graceful error handling

    def generate_summary(self):
        try:
            log.debug("=== Starting generate_summary ===")
            log.debug(f"Self.parsed_data type: {type(self.parsed_data)}")
            log.debug(f"Self.parsed_data full content: {self.parsed_data}")  # Added this line
            log.debug("=== Parsed Data Keys ===")
            if isinstance(self.parsed_data, dict):
                log.debug(f"Available keys: {list(self.parsed_data.keys())}")
                for key, value in self.parsed_data.items():
                    log.debug(f"Key: {key}")
                    log.debug(f"Value type: {type(value)}")
                    log.debug(f"Value content: {value}")
                    log.debug("---")
            else:
                log.error(f"parsed_data is not a dictionary but a {type(self.parsed_data)}")

            # Before creating sections
            if isinstance(self.parsed_data, dict):
                sections = self.parsed_data.get('sections', [])
                log.debug("=== Sections Debug ===")
                log.debug(f"Sections type: {type(sections)}")
                log.debug(f"Raw sections data: {sections}")
                log.debug(f"Number of sections before create_prompt: {len(sections)}")
                
                if isinstance(sections, list):
                    for i, section in enumerate(sections):
                        log.debug(f"Section {i} type: {type(section)}")
                        log.debug(f"Section {i} content: {section}")
                
                # Add pre-create_prompt debug
                log.debug("=== Pre create_prompt Debug ===")
                log.debug(f"About to call create_prompt with sections:")
                log.debug(f"Sections length: {len(sections)}")
                log.debug(f"Sections content: {sections}")
                
                summaries = self.create_prompt(sections)
                return summaries
                
        except Exception as e:
            log.error(f"Error in generate_summary: {str(e)}\n{traceback.format_exc()}")
            raise

    def create_prompt(self, sections):
        log.debug("==== Create Prompt Debug ====")
        log.debug(f"Number of sections: {len(sections)}")
        
        prompt = ""
        for i, section in enumerate(sections):
            log.debug(f"Processing section {i}: {section}")
            
            # Handle empty arrays
            if not section:
                log.debug(f"Section {i} is empty, skipping")
                continue
                
            if not isinstance(section, dict):
                log.warning(f"Section {i} is not a dictionary: {section}")
                continue
            
            # Try to get content first
            if 'content' in section and section['content']:
                content = section['content']
                if isinstance(content, list):
                    prompt += "\n".join(content) + "\n\n"
                else:
                    prompt += str(content) + "\n\n"
                log.debug(f"Using content for section {i}")
            # Fall back to secondary_title if content is missing or empty
            elif 'secondary_title' in section:
                prompt += section['secondary_title'] + "\n\n"
                log.debug(f"Using secondary_title for section {i}")
            else:
                log.warning(f"Section {i} has neither content nor secondary_title")
        
        return prompt
