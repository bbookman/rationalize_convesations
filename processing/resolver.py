from openai import OpenAI
import os

class AIEnhancedResolver:
    def __init__(self, bee_data, limitless_data):
        """Initialize resolver with Bee and Limitless summaries."""
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
        """Send a request to GPT-4o Mini to refine conflicting summaries."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI that merges conflicting summaries into a single refined version, preserving key details from both sources."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None  # Graceful error handling

    def resolve_conflicts(self):
        """Merge and refine summaries using OpenAI."""
        resolved_summaries = {}

        for filename in set(self.bee_data.keys()).union(self.limitless_data.keys()):
            bee_summary = self.bee_data.get(filename, "")
            limitless_summary = self.limitless_data.get(filename, "")

            if bee_summary and limitless_summary:
                # Create a structured prompt for OpenAI
                prompt = (
                    "Merge the following two summaries into a single coherent version while preserving key details:\n\n"
                    f"Summary from Bee:\n{bee_summary}\n\n"
                    f"Summary from Limitless:\n{limitless_summary}\n\n"
                    "Ensure the final summary is structured, avoids redundancy, and maintains key takeaways."
                )
                refined_summary = self.call_openai(prompt)
                resolved_summaries[filename] = refined_summary if refined_summary else "Error refining summary."
            else:
                resolved_summaries[filename] = bee_summary or limitless_summary  # Use whichever exists

        return resolved_summaries
