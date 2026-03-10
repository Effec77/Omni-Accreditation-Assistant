/**
 * Grade Calculator Utility
 * Maps confidence scores to letter grades with contextual information
 */

export interface GradeRange {
  min: number;
  max: number;
  grade: string;
  label: string;
  color: string;
  description: string;
}

export const GRADE_RANGES: GradeRange[] = [
  {
    min: 0,
    max: 0.3,
    grade: "C",
    label: "Weak",
    color: "text-red-500",
    description: "Significant gaps in evidence and documentation"
  },
  {
    min: 0.3,
    max: 0.5,
    grade: "B",
    label: "Developing",
    color: "text-orange-500",
    description: "Basic requirements met but needs improvement"
  },
  {
    min: 0.5,
    max: 0.7,
    grade: "B+",
    label: "Moderate",
    color: "text-yellow-500",
    description: "Good progress with some areas for enhancement"
  },
  {
    min: 0.7,
    max: 0.85,
    grade: "A",
    label: "Strong",
    color: "text-green-400",
    description: "Strong evidence with minor improvements possible"
  },
  {
    min: 0.85,
    max: 1.0,
    grade: "A+",
    label: "Excellent",
    color: "text-green-500",
    description: "Comprehensive evidence meeting all requirements"
  }
];

export interface GradeResult {
  grade: string;
  label: string;
  color: string;
  description: string;
  progressInRange: number;
  nextGrade: string | null;
  pointsToNextGrade: number | null;
}

/**
 * Calculate grade from confidence score
 */
export function calculateGrade(confidenceScore: number): GradeResult {
  // Clamp score between 0 and 1
  const score = Math.max(0, Math.min(1, confidenceScore));
  
  // Find matching grade range
  const gradeRange = GRADE_RANGES.find(
    range => score >= range.min && score < range.max
  ) || GRADE_RANGES[GRADE_RANGES.length - 1]; // Default to highest if score is 1.0
  
  // Calculate progress within current range
  const rangeSize = gradeRange.max - gradeRange.min;
  const progressInRange = rangeSize > 0 
    ? (score - gradeRange.min) / rangeSize 
    : 1;
  
  // Find next grade
  const currentIndex = GRADE_RANGES.indexOf(gradeRange);
  const nextGradeRange = currentIndex < GRADE_RANGES.length - 1 
    ? GRADE_RANGES[currentIndex + 1] 
    : null;
  
  const pointsToNextGrade = nextGradeRange 
    ? nextGradeRange.min - score 
    : null;
  
  return {
    grade: gradeRange.grade,
    label: gradeRange.label,
    color: gradeRange.color,
    description: gradeRange.description,
    progressInRange,
    nextGrade: nextGradeRange?.grade || null,
    pointsToNextGrade
  };
}

/**
 * Get color class for confidence score
 */
export function getScoreColor(score: number): string {
  const gradeRange = GRADE_RANGES.find(
    range => score >= range.min && score < range.max
  ) || GRADE_RANGES[GRADE_RANGES.length - 1];
  
  return gradeRange.color;
}

/**
 * Format confidence score as percentage
 */
export function formatConfidenceScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}
