import os
import re
import markdown
from bs4 import BeautifulSoup

class MarkdownParser:
    def __init__(self, bee_dir, limitless_dir):
        self.bee_dir = bee_dir
        self.limitless_dir = limitless_dir

    def extract_sections(self, file_path):
        """Extracts high-level and secondary summaries from a markdown file."""
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
            section_content = []

            # Find all secondary summaries (## headers) under this high-level summary
            next_sibling = header.find_next_sibling()
            while next_sibling and next_sibling.name != 'h1':
                if next_sibling.name == 'h2':
                    secondary_title = next_sibling.text.strip()
                    secondary_content = []

                    # Collect all paragraph content under this secondary summary
                    next_secondary_sibling = next_sibling.find_next_sibling()
                    while next_secondary_sibling and next_secondary_sibling.name not in ['h1', 'h2']:
                        if next_secondary_sibling.name == 'p':
                            secondary_content.append(next_secondary_sibling.text.strip())
                        next_secondary_sibling = next_secondary_sibling.find_next_sibling()

                    section_content.append({
                        "secondary_title": secondary_title,
                        "content": secondary_content
                    })
                next_sibling = next_sibling.find_next_sibling()

            sections[section_title] = section_content

        return sections

    def parse_markdown_files(self, directory):
        """Processes all markdown files in a directory."""
        parsed_data = {}
        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                file_path = os.path.join(directory, filename)
                parsed_data[filename] = self.extract_sections(file_path)
        return parsed_data

    def get_parsed_data(self):
        """Returns structured markdown data from both directories."""
        bee_data = self.parse_markdown_files(self.bee_dir)
        limitless_data = self.parse_markdown_files(self.limitless_dir)

        return {"bee": bee_data, "limitless": limitless_data}
