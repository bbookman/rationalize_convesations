import os

class SummaryGenerator:
    def __init__(self, summaries, output_dir):
        """Initialize generator with AI-generated summaries and output directory."""
        self.summaries = summaries
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure output directory exists

    def format_summary(self, summary_data, source_availability, location=None):
        """Format the summary into the required markdown structure."""
        formatted_summary = ""

        # Add Source Availability Note
        if source_availability:
            formatted_summary += f"**{source_availability}**\n\n"

        # Structure Summary Content
        if "summary" in summary_data:
            formatted_summary += f"# Best of Class Summary\n\n{summary_data['summary']}\n\n"
        
        if "highlights" in summary_data:
            formatted_summary += "## Conversation Highlights\n"
            for item in summary_data["highlights"][:5]:  # Max 5 bullets
                formatted_summary += f"- {item}\n"
            formatted_summary += "\n"

        if "key_takeaways" in summary_data:
            formatted_summary += "## Key Takeaways\n"
            for item in summary_data["key_takeaways"][:5]:  # Max 5 bullets
                formatted_summary += f"- {item}\n"
            formatted_summary += "\n"

        if "atmosphere" in summary_data:
            formatted_summary += f"## Atmosphere\n{summary_data['atmosphere']}\n\n"

        if "quotes" in summary_data:
            formatted_summary += "## Selected Quotes\n"
            for item in summary_data["quotes"][:6]:  # 3 impactful + 3 takeaway-aligned
                formatted_summary += f"- \"{item}\"\n"
            formatted_summary += "\n"

        # Add Location if Available
        if location:
            formatted_summary += f"**Location:** {location}\n\n"

        return formatted_summary.strip()

    def save_summary(self, date, summary_content):
        """Save formatted summary as a markdown file in the output directory."""
        filename = f"{self.output_dir}/{date}.md"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(summary_content)

    def generate_summaries(self):
        """Process and generate markdown summaries for all available data."""
        for source, files in self.summaries.items():
            for filename, summary_data in files.items():
                date = filename.replace(".md", "")

                # Determine source availability notation
                if "bee" in self.summaries and "limitless" in self.summaries:
                    source_availability = None  # Both sources exist
                elif "bee" in self.summaries:
                    source_availability = "Bee data only"
                elif "limitless" in self.summaries:
                    source_availability = "Limitless data only"
                else:
                    continue  # No valid data

                # Extract location if present
                location = summary_data.get("location")

                # Format and save summary
                formatted_summary = self.format_summary(summary_data, source_availability, location)
                self.save_summary(date, formatted_summary)

