"""
NAAC Evidence Quality Calculator
Calculates evidence quality assessment from individual criterion scores.

CALIBRATION FIX: This system measures EVIDENCE QUALITY, not actual NAAC grades.
- Your score (0-1): How much evidence text was found and how relevant it is
- NAAC score (1-4): Verified data submission quality assessed by DVV peer team

These are different measurements and should not be conflated.
"""

from typing import Dict, List, Any

# NAAC Criterion Weights (out of 1000 total points)
NAAC_CRITERION_WEIGHTS = {
    "1": 100,  # Curricular Aspects
    "2": 350,  # Teaching-Learning & Evaluation
    "3": 200,  # Research, Innovations & Extension
    "4": 100,  # Infrastructure & Learning Resources
    "5": 100,  # Student Support & Progression
    "6": 100,  # Governance, Leadership & Management
    "7": 50,   # Institutional Values & Best Practices
}

# Evidence Quality Bands (0-1 scale)
# CALIBRATION FIX: These are evidence quality bands, NOT NAAC grades
EVIDENCE_QUALITY_BANDS = [
    (0.85, 1.00, "Excellent", "Strong evidence with comprehensive documentation"),
    (0.70, 0.84, "Good", "Solid evidence with good documentation coverage"),
    (0.55, 0.69, "Moderate", "Adequate evidence but gaps in documentation"),
    (0.40, 0.54, "Weak", "Limited evidence with significant gaps"),
    (0.00, 0.39, "Insufficient", "Minimal or no evidence found"),
]


def get_criterion_number(criterion_id: str) -> str:
    """Extract criterion number from ID (e.g., '3.2.1' -> '3')"""
    return criterion_id.split('.')[0]


def confidence_to_grade_points(confidence: float) -> float:
    """
    Convert confidence score (0-1) to grade points (0-4) for internal calculation.
    
    CALIBRATION NOTE: This is for weighted averaging only.
    The final output should show evidence quality (0-1), not grade points.
    """
    # Simple linear mapping: 0.0 confidence = 0.0 points, 1.0 confidence = 4.0 points
    return confidence * 4.0


def get_evidence_quality_band(score: float) -> tuple:
    """Get evidence quality band and description from score (0-1 scale)."""
    for min_score, max_score, band, description in EVIDENCE_QUALITY_BANDS:
        if min_score <= score <= max_score:
            return band, description
    return "Insufficient", "Minimal or no evidence found"


# Legacy function for backward compatibility - maps to old grade system
# DEPRECATED: Use get_evidence_quality_band instead
def get_grade_from_cgpa(cgpa: float) -> tuple:
    """
    DEPRECATED: Maps CGPA to letter grades.
    This is misleading - use get_evidence_quality_band instead.
    """
    # Convert 0-4 scale back to 0-1 for evidence quality
    evidence_score = cgpa / 4.0
    return get_evidence_quality_band(evidence_score)


def calculate_naac_cgpa(criterion_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate overall evidence quality assessment from individual criterion results.
    
    CALIBRATION FIX: Returns evidence quality score (0-1), not NAAC CGPA.
    The output is renamed to reflect what we actually measure.
    
    Args:
        criterion_results: List of audit results for different criteria
        
    Returns:
        Dictionary with evidence quality score and assessment details
    """
    # Group results by main criterion (1, 2, 3, etc.)
    criterion_scores = {}
    criterion_details = {}
    
    for result in criterion_results:
        criterion_id = result.get('criterion', '')
        confidence = result.get('confidence_score', 0.0)
        
        # Extract main criterion number
        main_criterion = get_criterion_number(criterion_id)
        
        if not main_criterion or main_criterion not in NAAC_CRITERION_WEIGHTS:
            continue
        
        # Convert confidence to grade points for weighted averaging
        grade_points = confidence_to_grade_points(confidence)
        
        # Store for this criterion
        if main_criterion not in criterion_scores:
            criterion_scores[main_criterion] = []
            criterion_details[main_criterion] = []
        
        criterion_scores[main_criterion].append(grade_points)
        
        # Get evidence quality band for this metric
        quality_band, quality_desc = get_evidence_quality_band(confidence)
        
        criterion_details[main_criterion].append({
            'metric': criterion_id,
            'confidence': confidence,
            'grade_points': grade_points,
            'evidence_quality': quality_band,  # Changed from 'grade'
            'quality_description': quality_desc
        })
    
    # Calculate average grade points for each main criterion
    criterion_averages = {}
    for criterion, scores in criterion_scores.items():
        criterion_averages[criterion] = sum(scores) / len(scores) if scores else 0.0
    
    # Calculate weighted average (still using grade points internally)
    total_weighted_points = 0.0
    total_weight = 0
    
    for criterion, avg_grade_points in criterion_averages.items():
        weight = NAAC_CRITERION_WEIGHTS[criterion]
        total_weighted_points += avg_grade_points * weight
        total_weight += weight
    
    # Final score (convert back to 0-1 scale for evidence quality)
    cgpa_internal = total_weighted_points / total_weight if total_weight > 0 else 0.0
    evidence_quality_score = cgpa_internal / 4.0  # Convert 0-4 back to 0-1
    
    # Get evidence quality band
    quality_band, quality_description = get_evidence_quality_band(evidence_quality_score)
    
    # Build detailed breakdown
    breakdown = []
    for criterion in sorted(criterion_averages.keys()):
        avg_gp = criterion_averages[criterion]
        weight = NAAC_CRITERION_WEIGHTS[criterion]
        criterion_evidence_score = avg_gp / 4.0  # Convert to 0-1
        band, desc = get_evidence_quality_band(criterion_evidence_score)
        
        breakdown.append({
            'criterion': f"Criterion {criterion}",
            'average_grade_points': round(avg_gp, 2),
            'evidence_quality': band,  # Changed from 'grade'
            'evidence_score': round(criterion_evidence_score, 3),  # Added
            'weight': weight,
            'weighted_contribution': round((avg_gp * weight) / total_weight, 3),
            'metrics': criterion_details[criterion]
        })
    
    # CALIBRATION FIX: Return honest assessment of what we measured
    return {
        # Legacy fields (for backward compatibility with frontend)
        'cgpa': round(cgpa_internal, 2),  # Keep for internal calculation
        'letter_grade': quality_band,  # Now shows evidence quality band
        'description': quality_description,
        
        # New honest fields
        'evidence_quality_score': round(evidence_quality_score, 3),
        'evidence_quality_band': quality_band,
        'evidence_quality_description': quality_description,
        
        # Metadata
        'total_criteria_evaluated': len(criterion_averages),
        'total_metrics_evaluated': len(criterion_results),
        'breakdown': breakdown,
        
        # Updated status message
        'accreditation_status': (
            'Strong Evidence Base' if evidence_quality_score >= 0.70 else
            'Moderate Evidence Base' if evidence_quality_score >= 0.55 else
            'Weak Evidence Base' if evidence_quality_score >= 0.40 else
            'Insufficient Evidence'
        ),
        'grade_range': f"{evidence_quality_score:.2f} / 1.00",  # Changed to 0-1 scale
        
        # Disclaimer
        'disclaimer': (
            "This assessment measures evidence quality in uploaded documents. "
            "Final NAAC grade requires DVV peer team verification of data templates."
        )
    }


def get_improvement_suggestions(cgpa_result: Dict[str, Any]) -> List[str]:
    """Generate improvement suggestions based on evidence quality assessment."""
    suggestions = []
    
    evidence_score = cgpa_result.get('evidence_quality_score', cgpa_result.get('cgpa', 0) / 4.0)
    breakdown = cgpa_result['breakdown']
    
    # Find weakest criteria (evidence score < 0.55)
    weak_criteria = [
        b for b in breakdown 
        if b.get('evidence_score', b.get('average_grade_points', 0) / 4.0) < 0.55
    ]
    
    if weak_criteria:
        suggestions.append(
            f"Upload more documentation for {len(weak_criteria)} criterion/criteria with weak evidence: " +
            ", ".join([b['criterion'] for b in weak_criteria])
        )
    
    # Evidence quality improvement suggestions
    quality_band = cgpa_result.get('evidence_quality_band', cgpa_result.get('letter_grade', ''))
    
    if quality_band in ['Insufficient', 'Weak']:
        suggestions.append(
            "To improve evidence quality, focus on uploading comprehensive documents for "
            "high-weight criteria: Criterion 2 (Teaching-Learning, 350 points) and "
            "Criterion 3 (Research, 200 points)"
        )
        suggestions.append(
            "Ensure documents include: quantitative data, tables with metrics, "
            "policy documents, and achievement reports"
        )
    elif quality_band == 'Moderate':
        suggestions.append(
            "You have adequate evidence. To reach 'Good' quality (0.70+), "
            "add more detailed documentation with specific numbers, dates, and outcomes"
        )
    elif quality_band == 'Good':
        suggestions.append(
            "Strong evidence base! To reach 'Excellent' (0.85+), ensure all criteria "
            "have comprehensive documentation covering all required sub-metrics"
        )
    
    # Data completeness suggestions
    suggestions.append(
        "Remember: This assessment measures documentation quality. "
        "Final NAAC grade depends on DVV verification of your submitted data templates."
    )
    
    return suggestions
