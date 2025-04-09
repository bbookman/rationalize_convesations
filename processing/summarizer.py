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
            for key, value in self.parsed_data.items():
                log.debug(f"Key: {key}, Type: {type(value)}")
                if isinstance(value, (list, dict)):
                    log.debug(f"Content: {value}")

            # Before creating sections
            if isinstance(self.parsed_data, dict):
                sections = self.parsed_data.get('sections', [])
                log.debug("=== Sections Debug ===")
                log.debug(f"Sections type: {type(sections)}")
                log.debug(f"Sections content: {sections}")
                
                if isinstance(sections, list):
                    for i, section in enumerate(sections):
                        log.debug(f"Section {i} type: {type(section)}")
                        log.debug(f"Section {i} content: {section}")
            else:
                log.debug(f"parsed_data is not a dictionary: {type(self.parsed_data)}")
                raise TypeError(f"Expected dictionary, got {type(self.parsed_data)}")
            
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
