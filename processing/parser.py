import os
import re
import markdown
from bs4 import BeautifulSoup
import logging

log = logging.getLogger(__name__)

class MarkdownParser:
    def __init__(self, bee_dir, limitless_dir):
        self.bee_dir = bee_dir
        self.limitless_dir = limitless_dir
        

    def extract_sections(self, file_path):
        """Extracts high-level and secondary summaries from a markdown file."""
        log.debug(f"Extracting sections from {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()

        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract high-level summaries (# headers)
        high_level_headers = soup.find_all('h1')
        sections = {}  # Changed to dictionary

        for section_num, header in enumerate(high_level_headers):
            section_id = f'section_{section_num}'
            section = {
                'top_level_summary': header.text.strip(),
                'subsections': {}  # Changed to dictionary
            }
            
            # Find all secondary summaries (## headers) under this high-level summary
            next_sibling = header.find_next_sibling()
            subsection_num = 0
            
            while next_sibling and next_sibling.name != 'h1':
                if next_sibling.name == 'h2':
                    subsection_id = f'subsection_{section_num}_{subsection_num}'
                    subsection = {
                        'secondary_title': next_sibling.text.strip(),
                        'transcript': []  # Keep as list since it's sequential data
                    }
                    
                    # Collect all transcript lines under this secondary summary
                    next_transcript = next_sibling.find_next_sibling()
                    while next_transcript and next_transcript.name not in ['h1', 'h2']:
                        if next_transcript.name == 'p' and next_transcript.text.startswith('- '):
                            try:
                                line = next_transcript.text
                                speaker_part = line.split('(')[0].strip('- ')
                                timestamp = line[line.find('(')+1:line.find(')')]
                                content = line[line.find(':')+1:].strip() if ':' in line else ''
                                
                                transcript_entry = {
                                    'speaker': speaker_part.strip(),
                                    'timestamp': timestamp,
                                    'content': content
                                }
                                subsection['transcript'].append(transcript_entry)
                            except Exception as e:
                                log.warning(f"Failed to parse transcript line: {line}. Error: {e}")
                        
                        next_transcript = next_transcript.find_next_sibling()
                    
                    section['subsections'][subsection_id] = subsection  # Use dictionary assignment
                    subsection_num += 1
                
                next_sibling = next_sibling.find_next_sibling()

            sections[section_id] = section  # Use dictionary assignment

        log.debug(f"Found {len(sections)} main sections with their actual secondary titles")
        return sections

    def parse_markdown_files(self, directory):
        parsed_data = {}
        
        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                file_path = os.path.join(directory, filename)
                log.debug(f"Parsing file: {file_path}")
                
                # Always include filename as a key
                parsed_data[filename] = self.extract_sections(file_path)
                log.debug(f"Added data for {filename}")
                
        return parsed_data

    def get_parsed_data(self):
        """Returns structured markdown data from both directories."""
        log.debug("=== Starting get_parsed_data ===")
        try:
            log.debug("Reading bee directory...")
            bee_data = self.parse_markdown_files(self.bee_dir)
            log.debug("Reading limitless directory...")
            limitless_data = self.parse_markdown_files(self.limitless_dir)
            
            # Debug the structure
            log.debug(f"Bee data structure: {list(bee_data.keys())}")
            log.debug(f"Limitless data structure: {list(limitless_data.keys())}")
            
            return {"bee": bee_data, "limitless": limitless_data}
        except Exception as e:
            log.error(f"Error in parser: {e}")
            raise

    def parse_bee_file(self, content, filename):
        log.debug(f"Parsing Bee file: {filename}")
        conversations = []
        current_conversation = {}
        current_section = None
        
        lines = content.split('\n')
        i = 0
        
        # Define required sections
        REQUIRED_SECTIONS = {
            'second_level_summary': 'data missing',
            'key take aways': 'data missing',
            'atmosphere': 'data missing'
        }
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
                
            # Main conversation header (top level summary)
            if line.startswith('# '):
                if current_conversation:
                    # Add missing required sections before appending
                    for section, default_text in REQUIRED_SECTIONS.items():
                        if section not in current_conversation['sections']:
                            current_conversation['sections'][section] = [default_text]
                    conversations.append(current_conversation)
                
                current_conversation = {
                    'top_level_summary': line[2:].strip(),
                    'sections': {}
                }
                
            # Rest of parsing logic...
            # ...existing code for metadata and section parsing...
            
            i += 1
        
        # Handle final conversation
        if current_conversation:
            # Add missing required sections
            for section, default_text in REQUIRED_SECTIONS.items():
                if section not in current_conversation['sections']:
                    current_conversation['sections'][section] = [default_text]
            conversations.append(current_conversation)
        
        log.debug(f"Found {len(conversations)} conversations in {filename}")
        return conversations
