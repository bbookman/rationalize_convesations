import openai
import os
import toml

class AIEnhancedResolver:
    def __init__(self, bee_data, limitless_data):
        self.bee_data = bee_data
        self.limitless_data = limitless_data
        self.api_key = self.load_api_key()

    def load_api_key(self):
        """Load OpenAI API key from environment or config file."""
        config_path = "config.toml"
        if os.path.exists(config_path):
            config = toml.load(config_path)
            return config.get("openai", {}).get("api_key", "")
        return os.getenv("OPENAI_API_KEY", "")

    def call_openai(self, prompt):
        """Send a request to GPT-4o Mini for summarization."""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Refine the following summary while preserving key details."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

    def resolve_summaries(self):
        """Use AI to refine summaries while prioritizing Bee data."""
        resolved_summaries = {}
        for date, bee_summary in self.bee_data.items():
            limitless_summary = self.limitless_data.get(date, "")

            combined_summary = f"Bee Summary:\n{bee_summary}\n\nLimitless Summary:\n{limitless_summary}"
            refined_summary = self.call_openai(combined_summary) if limitless_summary else bee_summary

            resolved_summaries[date] = refined_summary
        return resolved_summaries

    def resolve_takeaways(self):
        """Use AI to merge and refine key takeaways intelligently."""
        resolved_takeaways = {}
        for date, bee_takeaways in self.bee_data.items():
            limitless_takeaways = self.limitless_data.get(date, [])

            combined_takeaways = "\n".join(bee_takeaways + limitless_takeaways)
            refined_takeaways = self.call_openai(combined_takeaways) if limitless_takeaways else "\n".join(bee_takeaways)

            resolved_takeaways[date] = refined_takeaways
        return resolved_takeaways
