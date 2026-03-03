"""
Test boundary detection patterns.
"""

import sys
from pathlib import Path
import re

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.semantic_chunker import NAAC_METRIC_HEADER_PATTERN, NAAC_WEIGHTAGE_PATTERN


def test_patterns():
    # Test text from page 63
    test_text = """zation for Research (20) Metric No. Weightage 3.2.1 QnM Extramural funding for Research (Grants sponsored by the non- government sources such as industry, corporate houses, international bodies for research projects) endowments, Chairs in the University during the last five years (INR in Lakhs) 3.2.1.1: Total Grants for research projects"""
    
    print("Test Text:")
    print(test_text[:200])
    print()
    
    print("Testing NAAC_METRIC_HEADER_PATTERN:")
    matches = list(NAAC_METRIC_HEADER_PATTERN.finditer(test_text))
    print(f"  Found {len(matches)} matches")
    for match in matches:
        print(f"    Position {match.start()}: '{match.group(0)}' -> ID: {match.group(1)}")
    print()
    
    print("Testing NAAC_WEIGHTAGE_PATTERN:")
    matches = list(NAAC_WEIGHTAGE_PATTERN.finditer(test_text))
    print(f"  Found {len(matches)} matches")
    for match in matches:
        print(f"    Position {match.start()}: '{match.group(0)}' -> ID: {match.group(1)}")
    print()
    
    # Test with newline before
    test_text2 = "\nWeightage 3.2.1 QnM Extramural funding"
    print("Test Text 2 (with newline):")
    print(repr(test_text2))
    print()
    
    print("Testing NAAC_METRIC_HEADER_PATTERN:")
    matches = list(NAAC_METRIC_HEADER_PATTERN.finditer(test_text2))
    print(f"  Found {len(matches)} matches")
    for match in matches:
        print(f"    Position {match.start()}: '{match.group(0)}' -> ID: {match.group(1)}")
    print()
    
    # Test simple pattern
    simple_pattern = re.compile(r'([1-7]\.\d{1,2}\.\d{1,2})\s+QnM')
    print("Testing simple pattern (no anchors):")
    matches = list(simple_pattern.finditer(test_text))
    print(f"  Found {len(matches)} matches")
    for match in matches:
        print(f"    Position {match.start()}: '{match.group(0)}' -> ID: {match.group(1)}")


if __name__ == "__main__":
    test_patterns()
