"""
NAAC Grading Calculator
Calculates overall NAAC grade (CGPA) from individual criterion scores.
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

# Grade ranges (CGPA on 4-point scale)
GRADE_RANGES = [
    (3.51, 4.00, "A++", "Outstanding"),
    (3.26, 3.50, "A+", "Excellent"),
    (3.01, 3.25, "A", "Very Good"),
    (2.76, 3.00, "B++", "Good"),
    (2.51, 2.75, "B+", "Above Average"),
    (2.01, 2.50, "B", "Average"),
    (1.51, 2.00, "C", "Below Average"),
    (0.00, 1.50, "D", "Poor"),
]


def get_criterion_number(criterion_id: str) -> str:
    """Extract criterion number from ID (e.g., '3.2.1' -> '3')"""
    return criterion_id.split('.')[0]


def confidence_to_grade_points(confidence: float) -> float:
    """
    Convert confidence score (0-1) to grade points (0-4).
    
    NAAC typically uses a 4-point scale where:
    - 4.0 = Excellent (85-100%)
    - 3.0 = Very Good (70-84%)
    - 2.0 = Good (55-69%)
    - 1.0 = Satisfactory (40-54%)
    - 0.0 = Unsatisfactory (<40%)
    """
    if confidence >= 0.85:
        return 4.0
    elif confidence >= 0.70:
        return 3.0 + (confidence - 0.70) / 0.15  # Linear interpolation 3.0-4.0
    elif confidence >= 0.55:
        return 2.0 + (confidence - 0.55) / 0.15  # Linear interpolation 2.0-3.0
    elif confidence >= 0.40:
        return 1.0 + (confidence - 0.40) / 0.15  # Linear interpolation 1.0-2.0
    else:
        return confidence / 0.40  # Linear interpolation 0.0-1.0


def get_grade_from_cgpa(cgpa: float) -> tuple:
    """Get letter grade and description from CGPA."""
    for min_cgpa, max_cgpa, grade, description in GRADE_RANGES:
        if min_cgpa <= cgpa <= max_cgpa:
            return grade, description
    return "D", "Poor"


def calculate_naac_cgpa(criterion_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate overall NAAC CGPA from individual criterion results.
    
    Args:
        criterion_results: List of audit results for different criteria
        
    Returns:
        Dictionary with CGPA, grade, and breakdown
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
        
        # Convert confidence to grade points
        grade_points = confidence_to_grade_points(confidence)
        
        # Store for this criterion
        if main_criterion not in criterion_scores:
            criterion_scores[main_criterion] = []
            criterion_details[main_criterion] = []
        
        criterion_scores[main_criterion].append(grade_points)
        criterion_details[main_criterion].append({
            'metric': criterion_id,
            'confidence': confidence,
            'grade_points': grade_points,
            'grade': result.get('grade', 'C')
        })
    
    # Calculate average grade points for each main criterion
    criterion_averages = {}
    for criterion, scores in criterion_scores.items():
        criterion_averages[criterion] = sum(scores) / len(scores) if scores else 0.0
    
    # Calculate weighted CGPA
    total_weighted_points = 0.0
    total_weight = 0
    
    for criterion, avg_grade_points in criterion_averages.items():
        weight = NAAC_CRITERION_WEIGHTS[criterion]
        total_weighted_points += avg_grade_points * weight
        total_weight += weight
    
    # Final CGPA (on 4-point scale)
    cgpa = total_weighted_points / total_weight if total_weight > 0 else 0.0
    
    # Get letter grade
    letter_grade, description = get_grade_from_cgpa(cgpa)
    
    # Build detailed breakdown
    breakdown = []
    for criterion in sorted(criterion_averages.keys()):
        avg_gp = criterion_averages[criterion]
        weight = NAAC_CRITERION_WEIGHTS[criterion]
        grade, desc = get_grade_from_cgpa(avg_gp)
        
        breakdown.append({
            'criterion': f"Criterion {criterion}",
            'average_grade_points': round(avg_gp, 2),
            'grade': grade,
            'weight': weight,
            'weighted_contribution': round((avg_gp * weight) / total_weight, 3),
            'metrics': criterion_details[criterion]
        })
    
    return {
        'cgpa': round(cgpa, 2),
        'letter_grade': letter_grade,
        'description': description,
        'total_criteria_evaluated': len(criterion_averages),
        'total_metrics_evaluated': len(criterion_results),
        'breakdown': breakdown,
        'accreditation_status': 'Accredited' if cgpa >= 1.51 else 'Not Accredited',
        'grade_range': f"{cgpa:.2f} / 4.00"
    }


def get_improvement_suggestions(cgpa_result: Dict[str, Any]) -> List[str]:
    """Generate improvement suggestions based on CGPA result."""
    suggestions = []
    
    cgpa = cgpa_result['cgpa']
    breakdown = cgpa_result['breakdown']
    
    # Find weakest criteria
    weak_criteria = [
        b for b in breakdown 
        if b['average_grade_points'] < 2.5
    ]
    
    if weak_criteria:
        suggestions.append(
            f"Focus on improving {len(weak_criteria)} weak criterion/criteria: " +
            ", ".join([b['criterion'] for b in weak_criteria])
        )
    
    # Target grade suggestions
    current_grade = cgpa_result['letter_grade']
    if current_grade in ['C', 'D', 'B']:
        suggestions.append(
            "To reach A+ grade (CGPA 3.26+), focus on high-weight criteria: "
            "Criterion 2 (Teaching-Learning, 350 points) and Criterion 3 (Research, 200 points)"
        )
    elif current_grade in ['B+', 'B++']:
        suggestions.append(
            "You're close to A grade! Strengthen documentation and evidence quality "
            "across all criteria to push CGPA above 3.01"
        )
    elif current_grade == 'A':
        suggestions.append(
            "To achieve A+ (CGPA 3.26+), enhance performance in Criterion 2 and 3, "
            "which carry the highest weights"
        )
    
    return suggestions
