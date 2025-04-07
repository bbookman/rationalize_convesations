from openai import OpenAI
import os

class AIEnhancedResolver:
    def __init__(self, bee_data, limitless_data):
        self.bee_data = bee_data
        self.limitless_data = limitless_data
        self.client = self.initialize_openai_client()

    def initialize_openai_client(self):
        """Initialize OpenAI client using environment variable."""
        api_key = os.getenv("OPENAI_API_KEY", "")
        
        if not api_key:
            raise ValueError("OpenAI API key is missing! Set OPENAI_API_KEY in your environment.")

        return OpenAI(api_key=api_key)

    def call_openai(self, prompt):
        """Send a request to GPT-4o Mini using OpenAI's updated API."""
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that refines summaries while preserving key details."},
                {"role": "user", "content": prompt}
            ]clea
        )
        return response.choices[0].message.content
