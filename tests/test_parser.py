import unittest
from processing.parser import MarkdownParser
import tempfile
import os

import sys
sys.path.append(os.path.abspath(".."))  # Add parent directory to module search path

from processing.parser import MarkdownParser



class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        """Create temporary directories and files for testing."""
        self.test_dir = tempfile.TemporaryDirectory()

        self.test_file_path = os.path.join(self.test_dir.name, "test.md")
        with open(self.test_file_path, "w", encoding="utf-8") as file:
            file.write("# Overall Summary\n\nThis is the summary.\n\n## Conversation 1\n\nDetails of conversation.\n")

        self.parser = MarkdownParser(self.test_dir.name, self.test_dir.name)

    def test_extract_sections(self):
        """Test if markdown headers and content are correctly parsed."""
        result = self.parser.extract_sections(self.test_file_path)
        expected_headers = ["Overall Summary", "Conversation 1"]
        expected_content = ["This is the summary.", "Details of conversation."]

        self.assertEqual(result["headers"], expected_headers)
        self.assertEqual(result["content"], expected_content)

    def tearDown(self):
        """Clean up temporary files."""
        self.test_dir.cleanup()

if __name__ == "__main__":
    unittest.main()
