import pytest
import os
from summarizer import AIEnhancedSummarizer
from parser import MarkdownParser


import sys
print(sys.path)


def test_summarizer():
    """Test AI summarizer with actual markdown files from predefined directories."""
    bee_dir = "test_data/bee"
    limitless_dir = "test_data/limitless"

    parser = MarkdownParser(bee_dir, limitless_dir)
    parsed_data = parser.get_parsed_data()

    summarizer = AIEnhancedSummarizer(parsed_data)
    summaries = summarizer.generate_summary()

    assert isinstance(summaries, dict), "Summaries should be a dictionary"
    
    for source, files in summaries.items():
        for filename, summary in files.items():
            assert isinstance(summary, str), f"Summary for {filename} in {source} should be a string"
            assert len(summary) > 0, f"Summary for {filename} should not be empty"

