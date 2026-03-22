"""
Semantic Dimension Checker - Framework-Driven Coverage Analysis
Compares institution evidence against NAAC/NBA framework requirements using semantic similarity.

This replaces hardcoded keyword matching with dynamic semantic comparison.
"""

from typing import List, Dict, Any, Tuple
import numpy as np


class SemanticDimensionChecker:
    """
    Check dimension coverage by comparing institution evidence against framework requirements.
    
    Instead of hardcoded keywords, this uses the actual NAAC/NBA framework chunks
    retrieved from the framework index as the ground truth.
    """
    
    def __init__(self, model_manager=None):
        """
        Initialize semantic dimension checker.
        
        Args:
            model_manager: ModelManager instance for embeddings
        """
        if model_manager is None:
            from models.model_manager import get_model_manager
            model_manager = get_model_manager()
        
        self.model_manager = model_manager
        self.embedding_model = model_manager.get_embedder()  # FIX: Correct method name
    
    def check(
        self,
        results: List[Dict[str, Any]],
        framework: str,
        criterion: str
    ) -> Dict[str, Any]:
        """
        Check dimension coverage using semantic comparison.
        
        Args:
            results: List of retrieval results (framework + institution chunks)
            framework: 'NAAC' or 'NBA'
            criterion: Criterion ID (e.g., '3.2.1')
            
        Returns:
            Coverage analysis with semantic matching
        """
        # Separate framework and institution chunks
        framework_chunks = [r for r in results if r.get('source_type') == 'framework']
        institution_chunks = [r for r in results if r.get('source_type') == 'institution']
        
        print(f"[SemanticDimensionChecker] Framework chunks: {len(framework_chunks)}")
        print(f"[SemanticDimensionChecker] Institution chunks: {len(institution_chunks)}")
        
        # If no framework chunks, fall back to basic coverage
        if not framework_chunks:
            return self._empty_coverage(criterion)
        
        # If no institution evidence, coverage = 0
        if not institution_chunks:
            requirements = self._extract_requirements(framework_chunks)
            return {
                'dimensions_covered': [],
                'dimensions_missing': requirements,
                'coverage_ratio': 0.0,
                'per_chunk_hits': {},
                'required_dimensions': requirements,
                'optional_dimensions': [],
                'metric_name': f"{framework} {criterion}",
                'institution_evidence_available': False,
                'framework_requirements': requirements
            }
        
        # Extract requirements from framework chunks
        requirements = self._extract_requirements(framework_chunks)
        
        # Match institution evidence against each requirement
        coverage_results = self._match_evidence_to_requirements(
            requirements,
            framework_chunks,
            institution_chunks
        )
        
        covered = coverage_results['covered']
        missing = coverage_results['missing']
        per_chunk_hits = coverage_results['per_chunk_hits']
        
        coverage_ratio = len(covered) / len(requirements) if requirements else 1.0
        
        return {
            'dimensions_covered': covered,
            'dimensions_missing': missing,
            'coverage_ratio': round(coverage_ratio, 3),
            'per_chunk_hits': per_chunk_hits,
            'required_dimensions': requirements,
            'optional_dimensions': [],
            'metric_name': f"{framework} {criterion}",
            'institution_evidence_available': True,
            'framework_requirements': requirements
        }
    
    def _extract_requirements(self, framework_chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Extract requirement dimensions from framework chunks.
        
        Args:
            framework_chunks: Framework chunks from retrieval
            
        Returns:
            List of requirement IDs/descriptions
        """
        requirements = []
        
        for chunk in framework_chunks:
            text = chunk.get('child_text', chunk.get('text', ''))
            
            # Extract key phrases that indicate requirements
            # Look for patterns like:
            # - "Number of projects"
            # - "Total funding amount"
            # - "Year-wise data"
            # - "Agency details"
            
            if any(keyword in text.lower() for keyword in [
                'number of', 'total', 'amount', 'year-wise', 'year wise',
                'agency', 'agencies', 'funding', 'grant', 'project'
            ]):
                # Extract the requirement phrase
                requirement = self._extract_requirement_phrase(text)
                if requirement and requirement not in requirements:
                    requirements.append(requirement)
        
        # If no specific requirements found, use generic ones
        if not requirements:
            requirements = [
                'funding_amount',
                'project_count',
                'funding_agencies',
                'time_period'
            ]
        
        return requirements
    
    def _extract_requirement_phrase(self, text: str) -> str:
        """
        Extract a concise requirement phrase from framework text.
        
        Args:
            text: Framework chunk text
            
        Returns:
            Requirement phrase
        """
        text_lower = text.lower()
        
        # Common requirement patterns
        if 'number of projects' in text_lower or 'projects funded' in text_lower:
            return 'project_count'
        elif 'total funding' in text_lower or 'amount' in text_lower:
            return 'funding_amount'
        elif 'agency' in text_lower or 'agencies' in text_lower:
            return 'funding_agencies'
        elif 'year-wise' in text_lower or 'year wise' in text_lower or 'last five years' in text_lower:
            return 'time_period'
        elif 'principal investigator' in text_lower or 'pi' in text_lower:
            return 'project_details'
        else:
            # Generic requirement based on first few words
            words = text.split()[:5]
            return '_'.join(words).lower()
    
    def _match_evidence_to_requirements(
        self,
        requirements: List[str],
        framework_chunks: List[Dict[str, Any]],
        institution_chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Match institution evidence against framework requirements using semantic similarity.
        
        Args:
            requirements: List of requirement IDs
            framework_chunks: Framework chunks
            institution_chunks: Institution chunks
            
        Returns:
            Coverage results with matched requirements
        """
        covered = []
        missing = []
        per_chunk_hits = {}
        
        # Get embeddings for framework chunks (requirements)
        framework_texts = [
            chunk.get('child_text', chunk.get('text', ''))
            for chunk in framework_chunks
        ]
        framework_embeddings = self.embedding_model.encode(framework_texts)
        
        # Get embeddings for institution chunks
        institution_texts = [
            chunk.get('child_text', chunk.get('text', ''))
            for chunk in institution_chunks
        ]
        institution_embeddings = self.embedding_model.encode(institution_texts)
        
        # For each requirement, find best matching institution evidence
        for req_idx, requirement in enumerate(requirements):
            # Find framework chunk that best represents this requirement
            req_framework_idx = self._find_requirement_chunk(
                requirement,
                framework_texts
            )
            
            if req_framework_idx is None:
                missing.append(requirement)
                continue
            
            # Compare this framework chunk against all institution chunks
            req_embedding = framework_embeddings[req_framework_idx]
            similarities = self._cosine_similarity(
                req_embedding,
                institution_embeddings
            )
            
            # If any institution chunk has high similarity (>0.6), requirement is covered
            max_similarity = np.max(similarities)
            best_match_idx = np.argmax(similarities)
            
            print(f"[SemanticDimensionChecker] Requirement '{requirement}': max_similarity={max_similarity:.3f}")
            
            if max_similarity > 0.6:  # Threshold for semantic match
                covered.append(requirement)
                
                # Track which institution chunk matched this requirement
                chunk_id = institution_chunks[best_match_idx].get('chunk_id', f'chunk_{best_match_idx}')
                if chunk_id not in per_chunk_hits:
                    per_chunk_hits[chunk_id] = []
                per_chunk_hits[chunk_id].append(requirement)
            else:
                missing.append(requirement)
        
        return {
            'covered': covered,
            'missing': missing,
            'per_chunk_hits': per_chunk_hits
        }
    
    def _find_requirement_chunk(
        self,
        requirement: str,
        framework_texts: List[str]
    ) -> int:
        """
        Find the framework chunk that best represents a requirement.
        
        Args:
            requirement: Requirement ID
            framework_texts: List of framework chunk texts
            
        Returns:
            Index of best matching framework chunk, or None
        """
        # Simple keyword matching for now
        requirement_lower = requirement.lower()
        
        for idx, text in enumerate(framework_texts):
            text_lower = text.lower()
            if requirement_lower in text_lower or any(
                word in text_lower for word in requirement_lower.split('_')
            ):
                return idx
        
        # If no match, return first chunk
        return 0 if framework_texts else None
    
    def _cosine_similarity(
        self,
        embedding1: np.ndarray,
        embeddings2: np.ndarray
    ) -> np.ndarray:
        """
        Calculate cosine similarity between one embedding and multiple embeddings.
        
        Args:
            embedding1: Single embedding vector
            embeddings2: Array of embedding vectors
            
        Returns:
            Array of similarity scores
        """
        # Normalize embeddings
        embedding1_norm = embedding1 / np.linalg.norm(embedding1)
        embeddings2_norm = embeddings2 / np.linalg.norm(embeddings2, axis=1, keepdims=True)
        
        # Calculate cosine similarity
        similarities = np.dot(embeddings2_norm, embedding1_norm)
        
        return similarities
    
    def _empty_coverage(self, criterion: str) -> Dict[str, Any]:
        """Return empty coverage result."""
        return {
            'dimensions_covered': [],
            'dimensions_missing': [],
            'coverage_ratio': 0.0,
            'per_chunk_hits': {},
            'required_dimensions': [],
            'optional_dimensions': [],
            'metric_name': criterion,
            'institution_evidence_available': False,
            'framework_requirements': []
        }
