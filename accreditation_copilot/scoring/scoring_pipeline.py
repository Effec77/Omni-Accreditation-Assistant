"""
C6 - Scoring Pipeline
Orchestrates the complete Phase 3 compliance reasoning pipeline.
"""

import time
from typing import List, Dict, Any

from .evidence_scorer import EvidenceScorer
from .semantic_dimension_checker import SemanticDimensionChecker  # NEW: Semantic checker
from .confidence_calculator import ConfidenceCalculator
from .synthesizer import ComplianceSynthesizer
from .output_formatter import OutputFormatter


class ScoringPipeline:
    """Complete Phase 3 scoring and reasoning pipeline."""
    
    def __init__(self, use_semantic_checker: bool = True):
        """
        Initialize all Phase 3 components.
        
        Args:
            use_semantic_checker: Use semantic dimension checker (default: True)
        """
        self.evidence_scorer = EvidenceScorer()
        
        # NEW: Use semantic dimension checker by default
        if use_semantic_checker:
            self.dimension_checker = SemanticDimensionChecker()
        else:
            from .dimension_checker import DimensionChecker
            self.dimension_checker = DimensionChecker()
        
        self.confidence_calculator = ConfidenceCalculator()
        self.synthesizer = ComplianceSynthesizer()
        self.output_formatter = OutputFormatter()
    
    def process(
        self,
        query: str,
        framework: str,
        criterion: str,
        retrieval_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Execute complete Phase 3 pipeline.
        
        Args:
            query: Original user query
            framework: 'NAAC' or 'NBA'
            criterion: Criterion ID (e.g., '3.2.1' or 'C5')
            retrieval_results: Output from Phase 2 retrieval
            
        Returns:
            Complete compliance report
        """
        start_time = time.time()
        
        # C1: Score evidence quality
        evidence_scores = self.evidence_scorer.score(retrieval_results)
        
        # C2: Check dimension coverage
        coverage = self.dimension_checker.check(retrieval_results, framework, criterion)
        
        # C3: Calculate confidence
        confidence = self.confidence_calculator.calculate(
            evidence_scores,
            coverage,
            retrieval_results
        )
        
        # C4: Generate synthesis (single LLM call)
        synthesis = self.synthesizer.generate(
            criterion,
            framework,
            confidence,
            coverage,
            retrieval_results,
            evidence_scores,
            user_query=query  # CRITICAL: Pass user's actual question
        )
        
        # C5: Format output
        latency = (time.time() - start_time) * 1000  # Convert to ms
        
        report = self.output_formatter.format(
            query,
            framework,
            criterion,
            confidence,
            coverage,
            synthesis,
            retrieval_results,
            evidence_scores,
            latency
        )
        
        return report
    
    def process_batch(
        self,
        queries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple queries in batch.
        
        Args:
            queries: List of query dicts with 'query', 'framework', 'criterion', 'results'
            
        Returns:
            List of compliance reports
        """
        reports = []
        
        for query_data in queries:
            report = self.process(
                query_data['query'],
                query_data['framework'],
                query_data['criterion'],
                query_data['results']
            )
            reports.append(report)
        
        return reports
