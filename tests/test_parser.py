import os
import unittest
from processing.parser import MarkdownParser  # Ensure this module exists and is accessible

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        """Initialize parser and create test markdown files dynamically."""
        self.bee_dir = "test_data/bee"
        self.limitless_dir = "test_data/limitless"
        os.makedirs(self.bee_dir, exist_ok=True)
        os.makedirs(self.limitless_dir, exist_ok=True)

        # Mock Bee markdown file
        self.bee_file = os.path.join(self.bee_dir, "test_bee.md")
        with open(self.bee_file, "w") as f:
            f.write(
                "# Bruce learned about the challenges his family faced in accessing mental health services\n\n"
                "## Summary\n\n"
                "Bruce explored options for mental health support beyond traditional clinical services.\n\n"
                "## Atmosphere\n\n"
                "The discussion was informative and supportive.\n\n"
                "## Key Take Aways\n\n"
                "- Alternative mental health resources\n"
                "- Ways to ensure accessibility\n"
            )

        # Mock Limitless markdown file
        self.limitless_file = os.path.join(self.limitless_dir, "test_limitless.md")
        with open(self.limitless_file, "w") as f:
            f.write(
                "# Bruce ensured his dog, Peach, was safe\n\n"
                "## Summary\n\n"
                "Bruce clarified instructions about retrieving something from a specific location.\n\n"
                "## Atmosphere\n\n"
                "The situation was urgent but manageable.\n\n"
                "## Key Take Aways\n\n"
                "- Importance of clear communication\n"
                "- Safety measures for pets\n"
            )

        # Initialize the parser with test directories
        self.parser = MarkdownParser(self.bee_dir, self.limitless_dir)

    def test_parse_markdown_files(self):
        """Ensure the parser extracts data from markdown files."""
        parsed_data = self.parser.parse_markdown_files("test_data/bee")

        # Validate that parsed data exists
        self.assertGreater(len(parsed_data.keys()), 0)

        # Validate structure per file
        for filename, sections in parsed_data.items():
            for high_level_title, sub_sections in sections.items():
                self.assertTrue(isinstance(high_level_title, str))

    def tearDown(self):
        """Clean up after tests."""
        os.remove(self.bee_file)
        os.remove(self.limitless_file)
        os.rmdir(self.bee_dir)
        os.rmdir(self.limitless_dir)

if __name__ == "__main__":
    unittest.main()
