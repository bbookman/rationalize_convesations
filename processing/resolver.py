import traceback
from processing.summarizer import AIEnhancedSummarizer
from utils.logger import log


class AIEnhancedResolver:
    def __init__(self, bee_data, limitless_data):
        self.bee_data = bee_data
        self.limitless_data = limitless_data
        log.debug(f"Resolver initialized with bee_data ({len(bee_data)} sections) and limitless_data ({len(limitless_data)} sections)")

    def resolve(self):
        """Resolves and combines data from both sources with Bee taking precedence"""
        log.debug("=== Starting Resolution Process ===")
        
        try:
            # Debug input data
            log.debug(f"Bee data structure: {self.bee_data}")
            log.debug(f"Limitless data structure: {self.limitless_data}")
            
            resolved_data = {
                'source_availability': [],
                'sections': []
            }

            # Check data availability
            has_bee = bool(self.bee_data)
            has_limitless = bool(self.limitless_data)
            
            if has_bee and has_limitless:
                resolved_data['source_availability'].append("Both sources available")
            elif has_bee:
                resolved_data['source_availability'].append("Bee data only")
            elif has_limitless:
                resolved_data['source_availability'].append("Limitless data only")
            else:
                log.warning("No data available from either source")
                return resolved_data

            # Process bee data first (primary source)
            for section_id, section_data in self.bee_data.items():
                log.debug(f"Processing bee section {section_id}: {section_data}")
                if isinstance(section_data, dict):
                    resolved_section = {
                        'section_id': section_id,
                        'source': 'bee',
                        'top_level_summary': section_data.get('top_level_summary', ''),
                        'secondary_title': section_data.get('secondary_title', 'No title'),
                        'content': section_data.get('content', [])
                    }
                    resolved_data['sections'].append(resolved_section)
                    log.debug(f"Added bee section: {resolved_section}")

            # Process limitless data
            for section_id, section_data in self.limitless_data.items():
                log.debug(f"Processing limitless section {section_id}: {section_data}")
                if isinstance(section_data, dict):
                    resolved_section = {
                        'section_id': section_id,
                        'source': 'limitless',
                        'top_level_summary': section_data.get('top_level_summary', ''),
                        'secondary_title': section_data.get('secondary_title', 'No title'),
                        'content': section_data.get('content', [])
                    }
                    resolved_data['sections'].append(resolved_section)
                    log.debug(f"Added limitless section: {resolved_section}")

            log.debug(f"Final resolved data: {resolved_data}")
            return resolved_data

        except Exception as e:
            log.error(f"Error during resolution: {str(e)}\n{traceback.format_exc()}")
            raise

    def resolve_conflicts(self):

        """Merge and refine summaries using OpenAI."""
        resolved_summaries = {}
        for filename in self.get_filenames():
            bee_summary = self.get_bee_summary(filename)
            log.debug(f"Bee summary for {filename}: {bee_summary}")
            limitless_summary = self.get_limitless_summary(filename)
            log.debug(f"Limitless summary for {filename}: {limitless_summary}")
            resolved_summary = self.merge_summaries(bee_summary, limitless_summary)
            resolved_summaries[filename] = resolved_summary
            log.debug(f"Resolved summary for {filename}: {resolved_summary}")
        return resolved_summaries

    def get_filenames(self):
        
        """Get the union of filenames from bee_data and limitless_data."""
        return set(self.bee_data.keys()).union(self.limitless_data.keys())

    def get_bee_summary(self, filename):
        
        """Get the summary from bee_data for the given filename."""
        return self.bee_data.get(filename, "")

    def get_limitless_summary(self, filename):
    
        """Get the summary from limitless_data for the given filename."""
        return self.limitless_data.get(filename, "")

    def merge_summaries(self, bee_summary, limitless_summary):
        
        """Merge the bee and limitless summaries using OpenAI."""
        if bee_summary and limitless_summary:
            log.debug("Both summaries are present, merging them.")
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