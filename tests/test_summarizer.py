import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import from the correct location
from processing.summarizer import AIEnhancedSummarizer

# Your test code here
def test_something():
    assert True
