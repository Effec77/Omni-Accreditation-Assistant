"""
Validation script for cross-metric contamination check.
Tests that no chunk labeled X.Y.Z contains another metric header.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingestion.semantic_chunker import validate_no_cross_metric_contamination


def main():
    db_path = "data/metadata.db"
    
    print("="*60)
    print("CROSS-METRIC CONTAMINATION VALIDATION")
    print("="*60)
    print()
    
    result = validate_no_cross_metric_contamination(db_path)
    
    if result:
        print("\n✅ VALIDATION PASSED")
        print("All chunks respect metric boundaries.")
        sys.exit(0)
    else:
        print("\n❌ VALIDATION FAILED")
        print("Cross-metric contamination detected.")
        sys.exit(1)


if __name__ == "__main__":
    main()
