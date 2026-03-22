"""
Test the criteria endpoint
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from criteria.criterion_registry import get_criteria

# Test the function directly
try:
    naac_criteria = get_criteria("NAAC")
    print(f"✓ NAAC Criteria Count: {len(naac_criteria)}")
    print("\nAvailable NAAC Criteria:")
    for crit in naac_criteria:
        print(f"  - {crit['criterion']}: {crit['description'][:60]}...")
    
    nba_criteria = get_criteria("NBA")
    print(f"\n✓ NBA Criteria Count: {len(nba_criteria)}")
    print("\nAvailable NBA Criteria:")
    for crit in nba_criteria:
        print(f"  - {crit['criterion']}: {crit['description'][:60]}...")
        
except Exception as e:
    print(f"✗ Error: {e}")
