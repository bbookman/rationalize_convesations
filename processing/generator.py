import os
from utils.logger import log
import traceback

class SummaryGenerator:
    def __init__(self, resolved_data, output_dir):
        self.resolved_data = resolved_data
        self.output_dir = output_dir
        log.debug(f"Generator initialized with output directory: {output_dir}")

    def generate(self):
        """Generates summary files based on resolved data"""
        log.debug("=== Starting Summary Generation ===")
        try:
            # Debug input data structure
            log.debug(f"Full resolved data: {self.resolved_data}")
            sections = self.resolved_data.get("sections", [])
            log.debug(f"Number of sections: {len(sections)}")

            content = []
            content.append("# Best of Class Summary\n")

            # Source availability
            source_note = "\n".join(self.resolved_data.get("source_availability", []))
            if source_note:
                content.append(f"*{source_note}*\n")

            # Conversation Highlights
            content.append("## Conversation Highlights")
            highlights = []
            for section in sections:
                log.debug(f"Processing section for highlights: {section}")
                if top_summary := section.get('top_level_summary'):
                    highlights.append(f"* {top_summary}")
                    log.debug(f"Added highlight: {top_summary}")
            if highlights:
                content.extend(highlights)
            content.append("\n")

            # Key Takeaways from Bee data
            content.append("## Key Takeaways")
            bee_sections = [s for s in sections if s.get('source') == 'bee']
            takeaways = []
            for section in bee_sections:
                log.debug(f"Processing bee section for takeaways: {section}")
                section_data = section.get('sections', {})
                for subsection in section_data.values():
                    if isinstance(subsection, dict) and 'key take aways' in subsection:
                        takeaways.extend(f"* {take}" for take in subsection['key take aways'])
            if takeaways:
                content.extend(takeaways[:5])
            content.append("\n")

            # Write output with verification
            output_path = os.path.join(self.output_dir, "summary.md")
            final_content = '\n'.join(content)
            log.debug(f"Final content to write:\n{final_content}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            log.debug(f"Summary written to: {output_path}")
            
        except Exception as e:
            log.error(f"Error generating summary: {str(e)}\n{traceback.format_exc()}")
            raise

