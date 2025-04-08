import os
import json
from utils.logger import Logger

class SummaryGenerator:
    def __init__(self, summaries, output_dir):
        """Initialize generator with AI-generated summaries and output directory."""
        self.summaries = self.process_summaries_structure(summaries)
        self.output_dir = output_dir
        self.logger = Logger()
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure output directory exists

    def process_summaries_structure(self, summaries):
        """Ensure summaries is a properly formatted dictionary."""
        print("Type of summaries:", type(summaries))
        if isinstance(summaries, str):
            try:
                summaries = json.loads(summaries)  # Convert string to dict if necessary
            except json.JSONDecodeError:
                raise ValueError("Summaries data is not valid JSON.")
            finally:
                self.logger.log(f"Summary JSON {summaries}")
        if not isinstance(summaries, dict):
            raise TypeError("Expected summaries to be a dictionary.")
        
        # Validate dictionary structure
        for source, files in summaries.items():
            if not isinstance(source, str):
                raise ValueError(f"Source key must be a string, got {type(source).__name__}")
            
            if not isinstance(files, (dict, list)):
                raise ValueError(f"Files for source '{source}' must be a dictionary or list, got {type(files).__name__}")
            
            if isinstance(files, dict):
                for filename, summary_data in files.items():
                    if not isinstance(summary_data, dict):
                        raise ValueError(f"Summary data for '{source}/{filename}' must be a dictionary, got {type(summary_data).__name__}")
                    
                    # Validate required fields in summary_data
                    required_fields = ["summary"]  # Add other required fields as needed
                    missing_fields = [field for field in required_fields if field not in summary_data]
                    if missing_fields:
                        raise ValueError(f"Summary data for '{source}/{filename}' is missing required fields: {', '.join(missing_fields)}")
        
        processed = {}  # Initialize the processed dictionary
        
        self.logger.log(f"Files: {files}")
        for source, files in summaries.items():
            if isinstance(files, list):
                processed[source] = {f"entry_{i}": v for i, v in enumerate(files)}
            else:
                processed[source] = files
        self.logger.log(f"Processed Summaries: {processed}")

        return processed

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
            if not isinstance(files, dict):
                print(f"Warning: Skipping {source}, expected dict but got {type(files).__name__}")
                with open(f"{self.output_dir}/{source}.md", "w", encoding="utf-8") as file:
                    file.write(f"Source: {source}") 
                continue

            for filename, summary_data in files.items():
                date = filename.replace(".md", "") if isinstance(filename, str) else f"entry_{filename}"

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
                location = summary_data.get("location", "Unknown")

                # Format and save summary
                formatted_summary = self.format_summary(summary_data, source_availability, location)
                self.save_summary(date, formatted_summary)

