import { AuditResult, Evidence, Dimension, Gap, Recommendation, Grade } from './audit';

// Component Props Interfaces

export interface GradeCalculatorProps {
  confidenceScore: number;  // 0-1 range
  criterionId: string;
  framework: string;
}

export interface EvidenceHumanizerProps {
  evidence: Evidence[];
  showTechnicalDetails?: boolean;
}

export interface ComparisonComponentProps {
  criterionId: string;
  dimensions: Dimension[];
  coverageRatio: number;
  framework: string;
}

export interface RecommendationEngineProps {
  auditResult: AuditResult;
}

export interface ConfidenceScoreVisualizerProps {
  score: number;  // 0-1 range
  showLabel?: boolean;
  showTooltip?: boolean;
  size?: "sm" | "md" | "lg";
}

export interface GapAnalysisVisualizerProps {
  gaps: Gap[];
  coverageRatio: number;
  dimensionsCovered: string[];
  dimensionsMissing: string[];
}

export interface EvidenceQualityIndicatorProps {
  strength: "strong" | "moderate" | "weak";
  showTooltip?: boolean;
}
