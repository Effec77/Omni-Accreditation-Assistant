/**
 * Recommendation Generator Utility
 * Generates contextual recommendations based on audit results
 */

export interface Recommendation {
  id: string;
  priority: "critical" | "high" | "medium";
  title: string;
  description: string;
  actionItems: string[];
  expectedImpact: string;
  category: "evidence" | "coverage" | "quality" | "specific";
}

/**
 * Generate recommendations for low confidence scores
 */
function generateLowConfidenceRecommendations(
  confidenceScore: number
): Recommendation[] {
  const recommendations: Recommendation[] = [];
  
  if (confidenceScore < 0.3) {
    recommendations.push({
      id: "low-confidence-critical",
      priority: "critical",
      title: "Strengthen Evidence Base",
      description: "Current evidence is insufficient to demonstrate compliance with NAAC standards.",
      actionItems: [
        "Conduct comprehensive documentation audit",
        "Gather missing evidence for all criteria",
        "Ensure all claims are backed by verifiable data",
        "Organize evidence by NAAC criterion for easy reference"
      ],
      expectedImpact: "Could improve score by 20-30 percentage points",
      category: "evidence"
    });
  } else if (confidenceScore < 0.5) {
    recommendations.push({
      id: "low-confidence-high",
      priority: "high",
      title: "Improve Evidence Quality",
      description: "Evidence exists but needs to be more comprehensive and better aligned with NAAC requirements.",
      actionItems: [
        "Review existing evidence for completeness",
        "Add quantitative data where qualitative exists",
        "Ensure evidence directly addresses criterion requirements",
        "Include recent data (within last 3 years)"
      ],
      expectedImpact: "Could improve score by 15-20 percentage points",
      category: "quality"
    });
  }
  
  return recommendations;
}

/**
 * Generate recommendations for missing dimensions
 */
function generateMissingDimensionRecommendations(
  missingDimensions: string[]
): Recommendation[] {
  const recommendations: Recommendation[] = [];
  
  if (missingDimensions.length > 0) {
    recommendations.push({
      id: "missing-dimensions",
      priority: "critical",
      title: `Address ${missingDimensions.length} Missing Dimension${missingDimensions.length > 1 ? 's' : ''}`,
      description: "Critical dimensions required by NAAC are not covered in current documentation.",
      actionItems: missingDimensions.map(dim => 
        `Provide evidence for: ${dim}`
      ),
      expectedImpact: "Essential for meeting minimum NAAC requirements",
      category: "coverage"
    });
  }
  
  return recommendations;
}

/**
 * Generate recommendations for quality improvement
 */
function generateQualityRecommendations(
  confidenceScore: number,
  coverageRatio: number
): Recommendation[] {
  const recommendations: Recommendation[] = [];
  
  // If coverage is 100% but confidence is still low, focus on quality
  if (coverageRatio === 1.0 && confidenceScore < 0.5) {
    recommendations.push({
      id: "quality-improvement",
      priority: "high",
      title: "Enhance Evidence Quality",
      description: "All dimensions are covered, but evidence quality needs improvement.",
      actionItems: [
        "Replace weak evidence with stronger documentation",
        "Add quantitative metrics and data points",
        "Include comparative analysis with benchmarks",
        "Provide detailed explanations and context"
      ],
      expectedImpact: "Could improve score by 10-15 percentage points",
      category: "quality"
    });
  }
  
  return recommendations;
}

/**
 * Generate criterion-specific recommendations
 */
function generateCriterionSpecificRecommendations(
  criterionId: string,
  confidenceScore: number
): Recommendation[] {
  const recommendations: Recommendation[] = [];
  
  // Example: Research-related criteria
  if (criterionId.startsWith("3.2") && confidenceScore < 0.7) {
    recommendations.push({
      id: "research-funding",
      priority: "high",
      title: "Strengthen Research Documentation",
      description: "Research and innovation criteria require comprehensive evidence of funding, publications, and impact.",
      actionItems: [
        "Document all research grants and funding sources",
        "Compile complete list of publications with citations",
        "Provide evidence of research impact and outcomes",
        "Include patents, collaborations, and consultancy projects"
      ],
      expectedImpact: "Critical for research-intensive institutions",
      category: "specific"
    });
  }
  
  // Example: Teaching-learning criteria
  if (criterionId.startsWith("2.") && confidenceScore < 0.7) {
    recommendations.push({
      id: "teaching-learning",
      priority: "high",
      title: "Enhance Teaching-Learning Evidence",
      description: "Teaching and learning criteria require detailed documentation of pedagogical practices and student outcomes.",
      actionItems: [
        "Document innovative teaching methods and practices",
        "Provide student performance data and trends",
        "Include evidence of continuous improvement initiatives",
        "Show faculty development and training programs"
      ],
      expectedImpact: "Essential for demonstrating educational quality",
      category: "specific"
    });
  }
  
  return recommendations;
}

/**
 * Main function to generate all recommendations
 */
export function generateRecommendations(
  confidenceScore: number,
  coverageRatio: number,
  missingDimensions: string[],
  criterionId: string
): Recommendation[] {
  const allRecommendations: Recommendation[] = [
    ...generateLowConfidenceRecommendations(confidenceScore),
    ...generateMissingDimensionRecommendations(missingDimensions),
    ...generateQualityRecommendations(confidenceScore, coverageRatio),
    ...generateCriterionSpecificRecommendations(criterionId, confidenceScore)
  ];
  
  // Sort by priority: critical > high > medium
  const priorityOrder = { critical: 0, high: 1, medium: 2 };
  return allRecommendations.sort(
    (a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]
  );
}

/**
 * Get top N most impactful recommendations
 */
export function getTopRecommendations(
  recommendations: Recommendation[],
  count: number = 3
): Recommendation[] {
  return recommendations.slice(0, count);
}

/**
 * Group recommendations by category
 */
export function groupRecommendationsByCategory(
  recommendations: Recommendation[]
): Record<string, Recommendation[]> {
  return recommendations.reduce((acc, rec) => {
    if (!acc[rec.category]) {
      acc[rec.category] = [];
    }
    acc[rec.category].push(rec);
    return acc;
  }, {} as Record<string, Recommendation[]>);
}
