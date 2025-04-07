import os
import re
import markdown
from bs4 import BeautifulSoup

class MarkdownParser:
    def __init__(self, bee_dir, limitless_dir):
        self.bee_dir = bee_dir
        self.limitless_dir = limitless_dir

    def extract_sections(self, file_path):
        """Extracts key sections (Overall summary, conversation summaries) from a markdown file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
        
        # Convert Markdown to HTML for easier parsing
        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, "html.parser")

        headers = [h.text for h in soup.find_all(['h1', 'h2'])]  # Extract markdown headers
        paragraphs = [p.text for p in soup.find_all('p')]  # Extract paragraph content

        return {"headers": headers, "content": paragraphs}

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
