"""
C3 - Confidence Calculator
Combines evidence strength and retrieval quality to produce confidence score.

FIXED: Multiplicative penalty for missing dimensions.
"""

from typing import List, Dict, Any


class ConfidenceCalculator:
    """Calculate confidence score and compliance status."""
    
    # Status thresholds
    THRESHOLDS = {
        'high': 0.75,
        'partial': 0.50,
        'weak': 0.25
    }
    
    def calculate(
        self,
        evidence_scores: List[Dict[str, Any]],
        coverage: Dict[str, Any],
        retrieval_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate confidence score and status.
        
        FIXED: Multiplicative penalty for missing dimensions.
        MILESTONE 5: Only use institution chunks for scoring (framework chunks are for LLM context only).
        
        Args:
            evidence_scores: Output from EvidenceScorer
            coverage: Output from DimensionChecker
            retrieval_results: Original Phase 2 results
            
        Returns:
            Confidence analysis with score and status
        """
        # MILESTONE 5: Filter to only institution chunks for scoring
        institution_indices = [
            i for i, r in enumerate(retrieval_results)
            if r.get('source_type') == 'institution'
        ]
        
        # Filter evidence scores to only institution chunks
        institution_evidence_scores = [
            evidence_scores[i] for i in institution_indices
            if i < len(evidence_scores)
        ]
        
        # Filter retrieval results to only institution chunks
        institution_retrieval_results = [
            retrieval_results[i] for i in institution_indices
        ]
        
        # If no institution evidence, return zero confidence
        if not institution_evidence_scores or not institution_retrieval_results:
            return {
                'confidence_score': 0.0,
                'status': 'Insufficient',
                'base_score': 0.0,
                'avg_evidence_score': 0.0,
                'avg_retrieval_score': 0.0,
                'coverage_ratio': 0.0
            }
        
        # Average evidence score (institution only)
        avg_evidence_score = (
            sum(e['evidence_score'] for e in institution_evidence_scores) / len(institution_evidence_scores)
        )
        
        # Average retrieval score (dense/FAISS) - institution only
        # CALIBRATION FIX: Use dense score instead of reranker score
        # BGE-reranker-base gives systematically low scores (0.03-0.04) on domain-specific text
        # Dense scores (FAISS cosine similarity) are more stable and well-calibrated
        total_dense_score = 0.0
        for r in institution_retrieval_results:
            # Try to get dense score first (preferred)
            score = r.get('dense_score', 0.0)
            if score == 0.0:
                # Try nested format
                score = r.get('scores', {}).get('dense', 0.0)
            if score == 0.0:
                # Fallback to reranker if dense not available
                score = r.get('reranker_score', 0.0)
                if score == 0.0:
                    score = r.get('scores', {}).get('reranker', 0.0)
            total_dense_score += score
        
        avg_retrieval_score = total_dense_score / len(institution_retrieval_results)
        
        # Base score: weighted combination - CALIBRATION FIX
        # Using dense scores which are more stable (0.85-0.99 for relevant matches)
        base_score = (
            0.6 * avg_evidence_score +   # Evidence quality from heuristics
            0.4 * avg_retrieval_score    # Dense similarity score (well-calibrated)
        )
        
        # Coverage ratio (FIXED: multiplicative penalty)
        coverage_ratio = coverage.get('coverage_ratio', 0.0)
        
        # Final confidence: base score × coverage ratio
        # This ensures missing dimensions penalize the score
        confidence_score = base_score * coverage_ratio
        
        # Determine status
        status = self._determine_status(confidence_score)
        
        return {
            'confidence_score': round(confidence_score, 3),
            'status': status,
            'base_score': round(base_score, 3),
            'avg_evidence_score': round(avg_evidence_score, 3),
            'avg_retrieval_score': round(avg_retrieval_score, 3),
            'coverage_ratio': round(coverage_ratio, 3)
        }
    
    def _determine_status(self, confidence_score: float) -> str:
        """Map confidence score to status."""
        if confidence_score >= self.THRESHOLDS['high']:
            return 'High'
        elif confidence_score >= self.THRESHOLDS['partial']:
            return 'Partial'
        elif confidence_score >= self.THRESHOLDS['weak']:
            return 'Weak'
        else:
            return 'Insufficient'
