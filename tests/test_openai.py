import unittest
from openai import OpenAI
import toml
import os

class TestOpenAIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize OpenAI client."""
        cls.api_key = os.getenv("OPENAI_API_KEY", "")

        if not cls.api_key and os.path.exists("config.toml"):
            config = toml.load("config.toml")
            cls.api_key = config.get("openai", {}).get("api_key", "")

        if not cls.api_key:
            raise ValueError("OpenAI API key is missing!")

        cls.client = OpenAI(api_key=cls.api_key)

    def test_openai_response(self):
        """Ensure OpenAI returns a valid response."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes information."},
                {"role": "user", "content": "Summarize the importance of AI in productivity."}
            ]
        )
        self.assertTrue(response.choices[0].message.content)  # Validate non-empty response

if __name__ == "__main__":
    unittest.main()
