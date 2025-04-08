import os
from openai import OpenAI



class AIEnhancedSummarizer:
    def __init__(self, parsed_data, api_key=None):
        """Initialize summarizer with parsed markdown data."""
        self.parsed_data = parsed_data
        self.api_key = os.getenv("OPENAI_API_KEY")  # Retrieve API key from environment
        

        if not self.api_key:
            raise ValueError("OpenAI API key is missing! Set OPENAI_API_KEY in your environment.")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def call_openai(self, prompt):
        
        """Send a request to GPT-4o Mini for enhanced summarization with error handling."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI tasked with generating refined summaries from parsed markdown data."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            return None  # Graceful error handling

    def generate_summary(self):
        
        """Iterate through parsed data and generate summaries for each section."""
        summaries = {}
        for source, data in self.parsed_data.items():
            summaries[source] = {}
            for filename, sections in data.items():
                prompt = self.create_prompt(sections)
                summary = self.call_openai(prompt)
                if summary:
                    summaries[source][filename] = summary
                else:
                    print(f"Failed to generate summary for {filename} in {source}")

        
        return summaries

    def create_prompt(self, sections):
        
        """Format extracted markdown data into a structured prompt for AI processing."""
        prompt = "Summarize the following markdown content into a structured overview:\n\n"
        for section_title, sub_sections in sections.items():
            prompt += f"## {section_title}\n"
            for sub in sub_sections:
                prompt += f"### {sub['secondary_title']}\n"
                prompt += "\n".join(sub["content"]) + "\n\n"
        return prompt.strip()
