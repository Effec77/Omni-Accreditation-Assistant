"""
C2 - Dimension Coverage Checker
Determines which required compliance dimensions are present in retrieved evidence.

FIXED: Per-chunk coverage tracking for traceability.
"""

import yaml
import os
from typing import List, Dict, Any, Set


class DimensionChecker:
    """Check coverage of required compliance dimensions."""
    
    def __init__(self, metric_maps_dir: str = None):
        """
        Initialize dimension checker with metric maps.
        
        Args:
            metric_maps_dir: Path to directory containing YAML metric maps
        """
        if metric_maps_dir is None:
            # Default to data/metric_maps relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            metric_maps_dir = os.path.join(
                os.path.dirname(current_dir),
                'data',
                'metric_maps'
            )
        
        self.metric_maps_dir = metric_maps_dir
        self.naac_map = self._load_yaml('naac_metric_map.yaml')
        self.nba_map = self._load_yaml('nba_metric_map.yaml')
    
    def _load_yaml(self, filename: str) -> Dict:
        """Load YAML metric map."""
        filepath = os.path.join(self.metric_maps_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Metric map not found: {filepath}")
            return {}
    
    def check(self, results: List[Dict[str, Any]], framework: str, criterion: str) -> Dict[str, Any]:
        """
        Check dimension coverage for a criterion.
        
        MILESTONE 5: Only count institution chunks as evidence.
        Framework chunks remain available for LLM context only.
        
        Args:
            results: List of retrieval results from Phase 2
            framework: 'NAAC' or 'NBA'
            criterion: Criterion ID (e.g., '3.2.1' or 'C5')
            
        Returns:
            Coverage analysis with per-chunk dimension hits
        """
        # Get metric definition
        metric_map = self.naac_map if framework == 'NAAC' else self.nba_map
        
        if framework not in metric_map:
            return self._empty_coverage()
        
        metric_def = metric_map[framework].get(criterion)
        if not metric_def:
            return self._empty_coverage()
        
        dimensions = metric_def.get('dimensions', [])
        if not dimensions:
            return self._empty_coverage()
        
        # MILESTONE 5: Filter to only institution chunks for evidence counting
        institution_chunks = [r for r in results if r.get('source_type') == 'institution']
        
        # If no institution evidence, coverage_ratio = 0
        if not institution_chunks:
            # Return zero coverage but keep framework chunks for LLM context
            required_dims = [d['id'] for d in dimensions if d.get('required', True)]
            optional_dims = [d['id'] for d in dimensions if not d.get('required', True)]
            
            return {
                'dimensions_covered': [],
                'dimensions_missing': required_dims,
                'coverage_ratio': 0.0,
                'per_chunk_hits': {},
                'required_dimensions': required_dims,
                'optional_dimensions': optional_dims,
                'metric_name': metric_def.get('name', 'Unknown'),
                'institution_evidence_available': False
            }
        
        # Check coverage PER CHUNK (only institution chunks)
        dimension_hits: Set[str] = set()
        per_chunk_hits: Dict[str, List[str]] = {}
        
        for result in institution_chunks:
            chunk_id = result.get('chunk_id', 'unknown')
            per_chunk_hits[chunk_id] = []
            
            # Combine child and parent text for checking
            text = (result.get('child_text', '') + ' ' + 
                   result.get('parent_context', '')).lower()
            
            # Check each dimension against THIS chunk
            for dimension in dimensions:
                dim_id = dimension['id']
                keywords = dimension.get('keywords', [])
                
                # Check if any keyword is present in THIS chunk
                if any(keyword.lower() in text for keyword in keywords):
                    dimension_hits.add(dim_id)
                    per_chunk_hits[chunk_id].append(dim_id)
        
        # Separate required and optional dimensions
        required_dims = [d['id'] for d in dimensions if d.get('required', True)]
        optional_dims = [d['id'] for d in dimensions if not d.get('required', True)]
        
        covered = list(dimension_hits)
        missing = [d for d in required_dims if d not in dimension_hits]
        
        # Calculate coverage ratio (only for required dimensions)
        coverage_ratio = (
            len([d for d in covered if d in required_dims]) / len(required_dims)
            if required_dims else 1.0
        )
        
        return {
            'dimensions_covered': covered,
            'dimensions_missing': missing,
            'coverage_ratio': round(coverage_ratio, 3),
            'per_chunk_hits': per_chunk_hits,
            'required_dimensions': required_dims,
            'optional_dimensions': optional_dims,
            'metric_name': metric_def.get('name', 'Unknown'),
            'institution_evidence_available': True
        }
    
    def _empty_coverage(self) -> Dict[str, Any]:
        """Return empty coverage result."""
        return {
            'dimensions_covered': [],
            'dimensions_missing': [],
            'coverage_ratio': 0.0,
            'per_chunk_hits': {},
            'required_dimensions': [],
            'optional_dimensions': [],
            'metric_name': 'Unknown'
        }
