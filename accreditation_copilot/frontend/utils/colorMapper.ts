/**
 * Color Mapper Utility
 * Maps confidence scores and other metrics to appropriate colors
 */

/**
 * Get Tailwind color class for confidence score
 */
export function getConfidenceColor(score: number): string {
  if (score >= 0.85) return "text-green-500";
  if (score >= 0.7) return "text-green-400";
  if (score >= 0.5) return "text-yellow-500";
  if (score >= 0.3) return "text-orange-500";
  return "text-red-500";
}

/**
 * Get background color class for confidence score
 */
export function getConfidenceBgColor(score: number): string {
  if (score >= 0.85) return "bg-green-500/20";
  if (score >= 0.7) return "bg-green-400/20";
  if (score >= 0.5) return "bg-yellow-500/20";
  if (score >= 0.3) return "bg-orange-500/20";
  return "bg-red-500/20";
}

/**
 * Get border color class for confidence score
 */
export function getConfidenceBorderColor(score: number): string {
  if (score >= 0.85) return "border-green-500";
  if (score >= 0.7) return "border-green-400";
  if (score >= 0.5) return "border-yellow-500";
  if (score >= 0.3) return "border-orange-500";
  return "border-red-500";
}

/**
 * Get color for evidence strength
 */
export function getStrengthColor(strength: "strong" | "moderate" | "weak"): string {
  switch (strength) {
    case "strong":
      return "text-green-500";
    case "moderate":
      return "text-yellow-500";
    case "weak":
      return "text-red-500";
  }
}

/**
 * Get background color for evidence strength
 */
export function getStrengthBgColor(strength: "strong" | "moderate" | "weak"): string {
  switch (strength) {
    case "strong":
      return "bg-green-500/20";
    case "moderate":
      return "bg-yellow-500/20";
    case "weak":
      return "bg-red-500/20";
  }
}

/**
 * Get color for recommendation priority
 */
export function getPriorityColor(priority: "critical" | "high" | "medium"): string {
  switch (priority) {
    case "critical":
      return "text-red-500";
    case "high":
      return "text-orange-500";
    case "medium":
      return "text-yellow-500";
  }
}

/**
 * Get background color for recommendation priority
 */
export function getPriorityBgColor(priority: "critical" | "high" | "medium"): string {
  switch (priority) {
    case "critical":
      return "bg-red-500/20";
    case "high":
      return "bg-orange-500/20";
    case "medium":
      return "bg-yellow-500/20";
  }
}

/**
 * Get color for coverage status
 */
export function getCoverageColor(ratio: number): string {
  if (ratio === 1.0) return "text-green-500";
  if (ratio >= 0.7) return "text-yellow-500";
  return "text-red-500";
}

/**
 * Get gradient class for confidence score (for progress bars)
 */
export function getConfidenceGradient(score: number): string {
  if (score >= 0.85) return "from-green-500 to-green-600";
  if (score >= 0.7) return "from-green-400 to-green-500";
  if (score >= 0.5) return "from-yellow-400 to-yellow-500";
  if (score >= 0.3) return "from-orange-400 to-orange-500";
  return "from-red-400 to-red-500";
}
