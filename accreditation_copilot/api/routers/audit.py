"""
Audit Router - Wraps CriterionAuditor and caching system
FIX 6: Standardized API responses
FIX 7: Structured logging for UI debugging
"""
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import logging

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from audit.criterion_auditor import CriterionAuditor
from models.model_manager import get_model_manager
from cache.audit_cache import AuditCache
from api.error_handler import standardize_audit_response, safe_audit_execution

# FIX 7: Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize components (singleton pattern)
model_manager = None
auditor = None
cache = None

def get_auditor():
    """Lazy initialization of auditor with ModelManager singleton"""
    global model_manager, auditor, cache
    if auditor is None:
        model_manager = get_model_manager()
        auditor = CriterionAuditor(model_manager=model_manager)
        cache = AuditCache()
    return auditor, cache

@router.get("/criteria/{framework}")
async def get_available_criteria(framework: str):
    """
    Get all available criteria for a framework.
    
    Args:
        framework: 'NAAC' or 'NBA'
        
    Returns:
        List of available criteria with descriptions
    """
    try:
        from criteria.criterion_registry import get_criteria
        
        framework_upper = framework.upper()
        criteria = get_criteria(framework_upper)
        
        return {
            "framework": framework_upper,
            "criteria": criteria,
            "count": len(criteria)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_grade(confidence_score: float, coverage_ratio: float) -> str:
    """
    Calculate NAAC/NBA grade based on confidence score only (matching frontend).
    
    Args:
        confidence_score: Overall confidence (0-1)
        coverage_ratio: Dimension coverage (0-1) - not used in calculation
        
    Returns:
        Grade string (A+, A, B+, B, C)
    """
    # Match frontend grade ranges exactly
    if confidence_score >= 0.85:
        return 'A+'
    elif confidence_score >= 0.70:
        return 'A'
    elif confidence_score >= 0.50:
        return 'B+'
    elif confidence_score >= 0.30:
        return 'B'
    else:
        return 'C'

def generate_personalized_recommendations(user_query: str, audit_result: dict, criterion: str, framework: str) -> list:
    """Generate personalized recommendations based on user's question and audit results"""
    try:
        model_manager = get_model_manager()
        groq_client = model_manager.get_groq_client()
        
        # Extract key info from audit
        confidence = audit_result.get('confidence_score', 0)
        coverage = audit_result.get('coverage_ratio', 0)
        grade = calculate_grade(confidence, coverage)
        missing_dims = audit_result.get('dimensions_missing', [])
        gaps = audit_result.get('gaps', [])
        compliance_status = audit_result.get('compliance_status', 'Unknown')
        evidence_count = audit_result.get('institution_evidence_count', 0)
        
        # Determine target grade
        grade_progression = {'C': 'B', 'B': 'B+', 'B+': 'A', 'A': 'A+', 'A+': 'A+'}
        target_grade = grade_progression.get(grade, 'A+')
        
        # Build detailed context for AI
        context = f"""
You are an expert NAAC/NBA accreditation consultant. A university has asked you this question:

"{user_query}"

Here is their current audit status for {framework} Criterion {criterion}:

CURRENT PERFORMANCE:
- Current Grade: {grade}
- Target Grade: {target_grade}
- Confidence Score: {confidence*100:.1f}%
- Coverage: {coverage*100:.1f}%
- Compliance Status: {compliance_status}
- Evidence Documents: {evidence_count} institutional documents found

GAPS IDENTIFIED:
{chr(10).join(f"- {gap}" for gap in gaps[:5]) if gaps else "- No major gaps identified"}

MISSING DIMENSIONS:
{chr(10).join(f"- {dim}" for dim in missing_dims) if missing_dims else "- All dimensions covered"}

YOUR TASK:
Provide a comprehensive, actionable answer to their question. Structure your response as follows:

1. DIRECT ANSWER (2-3 sentences addressing their specific question)

2. KEY ACTIONS (3-5 specific, measurable actions they should take)
   - Be concrete: include numbers, timelines, specific documents needed
   - Prioritize actions by impact

3. EXPECTED IMPACT
   - How will these actions improve their grade?
   - What score improvement can they expect?

4. TIMELINE
   - Short-term (1-3 months)
   - Medium-term (3-6 months)
   - Long-term (6-12 months)

5. BENCHMARKING
   - What do top-performing institutions do differently?
   - Specific examples from A+ institutions

Keep it practical, specific, and focused on moving from {grade} to {target_grade}.
"""
        
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert NAAC/NBA accreditation consultant. Provide detailed, actionable advice with specific numbers, timelines, and benchmarks."},
                {"role": "user", "content": context}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        recommendation_text = response.choices[0].message.content
        
        # Parse into structured format
        return [{
            "title": f"Personalized Roadmap: {grade} → {target_grade}",
            "description": recommendation_text,
            "priority": "High",
            "impact": f"Can improve grade from {grade} to {target_grade}",
            "current_grade": grade,
            "target_grade": target_grade,
            "actions": recommendation_text.split('\n')[:8]  # First 8 lines as actions
        }]
        
    except Exception as e:
        logger.error(f"Failed to generate personalized recommendations: {str(e)}")
        return []

class AuditRequest(BaseModel):
    framework: str  # "NAAC" or "NBA"
    criterion: str  # e.g., "3.2.1"
    query: Optional[str] = None  # Optional custom query

class AuditResponse(BaseModel):
    criterion: str
    framework: str
    compliance_status: str
    confidence_score: float
    coverage_ratio: float
    evidence_count: int
    evidence: list
    gaps: list
    grounding: dict
    dimensions_covered: list
    dimensions_missing: list
    recommendations: list
    explanation: str
    timestamp: str
    cached: bool = False
    grade: Optional[str] = None
    personalized_recommendations: Optional[list] = None
    user_query: Optional[str] = None

@router.post("/run", response_model=AuditResponse)
async def run_audit(request: AuditRequest):
    """
    Run audit for a specific criterion.
    Uses caching automatically.
    
    FIX 6: Standardized response format
    FIX 7: Structured logging for debugging
    """
    try:
        # FIX 7: Log audit start
        logger.info(f"[AUDIT START] Framework: {request.framework}, Criterion: {request.criterion}")
        
        auditor, cache = get_auditor()
        
        # Get criterion details from registry
        from criteria.criterion_registry import get_criteria
        # Convert framework to uppercase for consistency
        framework_upper = request.framework.upper()
        criteria = get_criteria(framework_upper)
        criterion_def = next((c for c in criteria if c['criterion'] == request.criterion), None)
        
        if not criterion_def:
            raise HTTPException(status_code=404, detail=f"Criterion {request.criterion} not found for {request.framework}")
        
        # ALWAYS use the criterion template for audit (ignore user query for scoring)
        query_template = criterion_def['query_template']
        
        # Run audit with caching enabled
        # Pass user query if provided to influence synthesis
        result = auditor.audit_criterion(
            criterion_id=request.criterion,
            framework=framework_upper,
            query_template=query_template,
            description=criterion_def['description'],
            user_query=request.query if request.query else ""
        )
        
        # If user provided a custom query, generate personalized recommendations
        if request.query and request.query.strip():
            logger.info(f"[CUSTOM QUERY] Generating personalized recommendations for: {request.query}")
            try:
                personalized_recs = generate_personalized_recommendations(
                    user_query=request.query,
                    audit_result=result,
                    criterion=request.criterion,
                    framework=framework_upper
                )
                # Add personalized recommendations to the result
                result['personalized_recommendations'] = personalized_recs
                result['user_query'] = request.query
            except Exception as e:
                logger.error(f"[CUSTOM QUERY ERROR] {str(e)}")
                # Don't fail the audit if recommendation generation fails
                result['personalized_recommendations'] = []
        
        # FIX 7: Log retrieval count
        evidence_count = result.get("evidence_count", 0)
        logger.info(f"[RETRIEVAL] Retrieved {evidence_count} evidence chunks")
        
        # FIX 7: Log compliance scoring complete
        compliance_status = result.get("compliance_status", "unknown")
        confidence_score = result.get("confidence_score", 0.0)
        logger.info(f"[COMPLIANCE] Status: {compliance_status}, Confidence: {confidence_score:.2f}")
        
        # Check if result was cached
        cached = result.get("cached", False)
        
        # FIX 7: Log audit completion
        logger.info(f"[AUDIT COMPLETE] Criterion: {request.criterion}, Cached: {cached}")
        
        # FIX 6: Standardize response
        standardized = standardize_audit_response(result)
        
        # Calculate grade
        grade = calculate_grade(
            standardized.get("confidence_score", 0.0),
            standardized.get("coverage_ratio", 0.0)
        )
        
        # Add grade to result
        standardized['grade'] = grade
        
        # Debug logging
        logger.info(f"[GRADE CALCULATION] Confidence: {standardized.get('confidence_score', 0.0):.3f}, Grade: {grade}")
        
        # If personalized recommendations were generated, add them to standardized
        if 'personalized_recommendations' in result:
            standardized['personalized_recommendations'] = result['personalized_recommendations']
            standardized['user_query'] = result.get('user_query', '')
        
        return AuditResponse(
            criterion=request.criterion,
            framework=request.framework,
            compliance_status=standardized.get("compliance_status", "unknown"),
            confidence_score=standardized.get("confidence_score", 0.0),
            coverage_ratio=standardized.get("coverage_ratio", 0.0),
            evidence_count=standardized.get("evidence_count", 0),
            evidence=standardized.get("evidence_sources", []),
            gaps=standardized.get("gaps", []),
            grounding={
                "dimension_grounding": standardized.get("dimension_grounding", []),
                "gaps_identified": standardized.get("gaps_identified", []),
                "evidence_strength": standardized.get("evidence_strength", {})
            },
            dimensions_covered=standardized.get("dimensions_covered", []),
            dimensions_missing=standardized.get("dimensions_missing", []),
            recommendations=standardized.get("recommendations", []),
            explanation=standardized.get("explanation", ""),
            timestamp=datetime.now().isoformat(),
            cached=cached,
            grade=grade,
            personalized_recommendations=standardized.get('personalized_recommendations', []),
            user_query=standardized.get('user_query', '')
        )
        
    except Exception as e:
        # FIX 7: Log error
        logger.error(f"[AUDIT ERROR] {request.criterion}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-full-audit")
async def run_full_naac_audit():
    """
    Run audit for ALL NAAC criteria and calculate overall CGPA/grade.
    This is the main endpoint for comprehensive NAAC accreditation assessment.
    """
    try:
        from criteria.criterion_registry import get_criteria
        from scoring.naac_grading import calculate_naac_cgpa, get_improvement_suggestions
        
        logger.info("[FULL AUDIT START] Running comprehensive NAAC audit")
        
        auditor, cache = get_auditor()
        
        # Get all NAAC criteria
        naac_criteria = get_criteria("NAAC")
        
        # Run audit for each criterion
        results = []
        for criterion_def in naac_criteria:
            criterion_id = criterion_def['criterion']
            
            logger.info(f"[FULL AUDIT] Processing criterion {criterion_id}")
            
            try:
                result = auditor.audit_criterion(
                    criterion_id=criterion_id,
                    framework="NAAC",
                    query_template=criterion_def['query_template'],
                    description=criterion_def['description'],
                    user_query=""
                )
                
                # Standardize response
                standardized = standardize_audit_response(result)
                
                # Calculate grade
                grade = calculate_grade(
                    standardized.get("confidence_score", 0.0),
                    standardized.get("coverage_ratio", 0.0)
                )
                
                standardized['grade'] = grade
                standardized['criterion'] = criterion_id
                
                results.append(standardized)
                
            except Exception as e:
                logger.error(f"[FULL AUDIT ERROR] Criterion {criterion_id}: {str(e)}")
                # Continue with other criteria even if one fails
                continue
        
        # Calculate overall NAAC CGPA
        cgpa_result = calculate_naac_cgpa(results)
        
        # Get improvement suggestions
        suggestions = get_improvement_suggestions(cgpa_result)
        
        logger.info(f"[FULL AUDIT COMPLETE] CGPA: {cgpa_result['cgpa']}, Grade: {cgpa_result['letter_grade']}")
        
        return {
            "audit_type": "full_naac_audit",
            "framework": "NAAC",
            "timestamp": datetime.now().isoformat(),
            "overall_result": cgpa_result,
            "improvement_suggestions": suggestions,
            "individual_criteria": results,
            "summary": {
                "total_criteria": len(naac_criteria),
                "criteria_evaluated": cgpa_result['total_criteria_evaluated'],
                "metrics_evaluated": cgpa_result['total_metrics_evaluated'],
                "cgpa": cgpa_result['cgpa'],
                "grade": cgpa_result['letter_grade'],
                "accreditation_status": cgpa_result['accreditation_status']
            }
        }
        
    except Exception as e:
        logger.error(f"[FULL AUDIT ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache")
async def get_cached_audits():
    """
    Retrieve all cached audit results.
    """
    try:
        _, cache = get_auditor()
        
        # Get cache statistics
        stats = cache.get_stats()
        
        # List cached audits
        cached_audits = []
        # Note: Implement cache listing in AuditCache if needed
        
        return {
            "stats": stats,
            "audits": cached_audits
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cache")
async def clear_cache():
    """
    Clear all cached audit results.
    """
    try:
        _, cache = get_auditor()
        cache.clear()
        
        return {"message": "Cache cleared successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
