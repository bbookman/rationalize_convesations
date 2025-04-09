import os
import traceback
from openai import OpenAI
from utils.logger import log
from nested_lookup import nested_lookup

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
            
            # Look for sections in nested structure
            log.debug("Searching for sections in nested structure...")
            all_sections = []
            
            # Search through bee and limitless data
            for key in ['bee', 'limitless']:
                if key in self.parsed_data:
                    date_data = self.parsed_data[key]
                    log.debug(f"Processing {key} data...")
                    log.debug(f"date_data type: {type(date_data)}")
                    log.debug(f"date_data keys: {date_data.keys()}")
                    
                    # Each section should be a dictionary with title and content
                    for filename, file_data in date_data.items():
                        log.debug(f"\nProcessing file: {filename}")
                        log.debug(f"file_data type: {type(file_data)}")
                        log.debug(f"file_data keys: {file_data.keys() if isinstance(file_data, dict) else 'NOT A DICT'}")
                        
                        for section_id, section_data in file_data.items():
                            log.debug(f"\nProcessing section_id: {section_id}")
                            log.debug(f"section_data type: {type(section_data)}")
                            log.debug(f"section_data content: {section_data}")
                            
                            if not isinstance(section_data, dict):
                                log.error(f"Found non-dictionary section_data: {type(section_data)}")
                                log.error(f"Value: {section_data}")
                                continue
                                
                            section = {
                                'section_id': section_id,
                                'source': key,
                                'secondary_title': section_data.get('secondary_title', 'No title'),
                                'transcript': section_data.get('transcript', []),
                                'content': section_data.get('content', [])
                            }
                            all_sections.append(section)
                            log.debug(f"Added section: {section}")
                
            log.debug(f"\nTotal sections found: {len(all_sections)}")
            return self.create_prompt(all_sections)
                
        except Exception as e:
            log.error(f"Error in generate_summary: {str(e)}\n{traceback.format_exc()}")
            raise

    def create_prompt(self, sections):
        log.debug("==== Create Prompt Debug ====")
        log.debug(f"Number of sections: {len(sections)}")
        
        result = {
            'bee': {},
            'limitless': {}
        }
        
        for section in sections:
            log.debug(f"Processing section: {section}")
            
            if not isinstance(section, dict):
                log.warning(f"Section is not a dictionary: {section}")
                continue
                
            source = section['source']
            section_id = section['section_id']
            
            # Get the actual data from the nested section structure
            section_data = section.get('sections', {})  # Get the sections dictionary
            secondary_title = None
            transcript = []
            content = []
            
            # Get data from subsections
            for subsection_id, subsection in section_data.items():
                log.debug(f"Processing subsection: {subsection}")
                if subsection.get('secondary_title'):
                    secondary_title = subsection['secondary_title']
                if subsection.get('transcript'):
                    transcript.extend(subsection['transcript'])
            
            # Create section with actual content
            result[source][section_id] = {
                'top_level_summary': section.get('top_level_summary', ''),
                'secondary_title': secondary_title or 'No title',
                'transcript': transcript,
                'content': content
            }
            log.debug(f"Added section {section_id} to {source} with actual content")
        
        log.debug(f"Final structure - bee sections: {len(result['bee'])}, limitless sections: {len(result['limitless'])}")
        return result
