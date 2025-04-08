import os
import re
import markdown
from bs4 import BeautifulSoup
from utils.logger import Logger

class MarkdownParser:
    def __init__(self, bee_dir, limitless_dir):
        self.bee_dir = bee_dir
        self.limitless_dir = limitless_dir
        self.logger = Logger()
        self.logger.log_info("MarkdownParser initialized with directories: {}, {}".format(bee_dir, limitless_dir))

    def extract_sections(self, file_path):
        """Extracts high-level and second`ary summaries from a markdown file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()

        # Convert Markdown to HTML for easier parsing
        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract high-level summaries (# headers)
        high_level_headers = soup.find_all('h1')
        sections = {}

        for header in high_level_headers:
            section_title = header.text.strip()
            self.logger.log_info("Processing section: {}".format(section_title))
            # Initialize a list to hold secondary summaries
            section_content = []

            # Find all secondary summaries (## headers) under this high-level summary
            next_sibling = header.find_next_sibling()
            while next_sibling and next_sibling.name != 'h1':
                if next_sibling.name == 'h2':
                    secondary_title = next_sibling.text.strip()
                    self.logger.log_info("Processing secondary summary: {}".format(secondary_title))
                    secondary_content = []

                    # Collect all paragraph content under this secondary summary
                    next_secondary_sibling = next_sibling.find_next_sibling()
                    while next_secondary_sibling and next_secondary_sibling.name not in ['h1', 'h2']:
                        if next_secondary_sibling.name == 'p':
                            secondary_content.append(next_secondary_sibling.text.strip())
                        next_secondary_sibling = next_secondary_sibling.find_next_sibling()
                    if not secondary_content:
                                 section_content.append({
                        "secondary_title": secondary_title, })
                    else: 
                        section_content.append({
                            "secondary_title": secondary_title,
                            "content": secondary_content
                        })
                next_sibling = next_sibling.find_next_sibling()

            sections[section_title] = section_content
            self.logger.log_info("Completed processing section: {}".format(sections[section_title]))
        self.logger.log_info("Sections extracted: {}".format(sections))
        
        return sections

    def parse_markdown_files(self, directory):
        """Processes all markdown files in a directory."""
        parsed_data = {}
        for filename in os.listdir(directory):
            
            if filename.endswith(".md"):
                self.logger.log_info("Processing file: {}".format(filename))
                file_path = os.path.join(directory, filename)

                parsed_data[filename] = self.extract_sections(file_path)
        Logger().log_info("Parsed data: {}".format(parsed_data))        
        return parsed_data
    def get_parsed_data(self):
        """Returns structured markdown data from both directories."""
        bee_data = self.parse_markdown_files(self.bee_dir)
        limitless_data = self.parse_markdown_files(self.limitless_dir)


        return {"bee": bee_data, "limitless": limitless_data}
