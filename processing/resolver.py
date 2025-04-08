from processing.summarizer import AIEnhancedSummarizer
from utils.logger import Logger

class AIEnhancedResolver:
    def __init__(self, bee_data, limitless_data):
        self.bee_data = bee_data
        self.limitless_data = limitless_data
        self.loogger = Logger()

    def resolve_conflicts(self):
        self.loogger.log("info"),("Starting conflict resolution...")
        """Merge and refine summaries using OpenAI."""
        resolved_summaries = {}
        for filename in self.get_filenames():
            bee_summary = self.get_bee_summary(filename)
            limitless_summary = self.get_limitless_summary(filename)
            resolved_summary = self.merge_summaries(bee_summary, limitless_summary)
            resolved_summaries[filename] = resolved_summary
        return resolved_summaries

    def get_filenames(self):
        self.loogger.log("info"),("Getting filenames...")
        """Get the union of filenames from bee_data and limitless_data."""
        return set(self.bee_data.keys()).union(self.limitless_data.keys())

    def get_bee_summary(self, filename):
        self.loogger.log("info"),("Getting bee summary...")
        """Get the summary from bee_data for the given filename."""
        return self.bee_data.get(filename, "")

    def get_limitless_summary(self, filename):
        self.loogger.log("info"),("Getting limitless summary...")
        """Get the summary from limitless_data for the given filename."""
        return self.limitless_data.get(filename, "")

    def merge_summaries(self, bee_summary, limitless_summary):
        self.loogger.log("info"),("Merging summaries...")
        """Merge the bee and limitless summaries using OpenAI."""
        if bee_summary and limitless_summary:
            prompt = self.create_prompt(bee_summary, limitless_summary)
            summarizer = AIEnhancedSummarizer(None)  # Create an instance of AIEnhancedSummarizer
            refined_summary = summarizer.call_openai(prompt)
            return refined_summary if refined_summary else "Error refining summary."
        else:
            return bee_summary or limitless_summary

    def create_prompt(self, bee_summary, limitless_summary):
        """Create a structured prompt for OpenAI."""
        return (
            "Merge the following two summaries into a single coherent version while preserving key details:\n\n"
            f"Summary from Bee:\n{bee_summary}\n\n"
            f"Summary from Limitless:\n{limitless_summary}\n\n"
            "Ensure the final summary is structured, avoids redundancy, and maintains key takeaways."
        )