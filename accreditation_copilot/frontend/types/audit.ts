// Audit Result Types
export interface AuditResult {
  // Identification
  criterion: string;
  framework: string;
  timestamp: string;
  cached: boolean;
  
  // Compliance Metrics
  compliance_status: "Compliant" | "Partial" | "Weak" | "No Evidence" | "Timeout";
  confidence_score: number;  // 0-1
  coverage_ratio: number;    // 0-1
  
  // Evidence
  evidence_count: number;
  evidence: Evidence[];
  
  // Dimensions
  dimensions_covered: string[];
  dimensions_missing: string[];
  
  // Analysis
  gaps: string[];
  grounding: {
    dimension_grounding: DimensionGrounding[];
    gaps_identified: string[];
    evidence_strength: Record<string, string>;
  };
  
  // Recommendations
  recommendations: string[];
  explanation: string;
}

export interface Evidence {
  // Raw backend fields
  child_text?: string;
  text?: string;
  reranker_score?: number;
  metadata?: {
    source: string;
    page_number?: number;
    chunk_id?: string;
    doc_type?: string;
  };
  source?: string;
  page?: number;
  
  // Computed fields
  strength?: "strong" | "moderate" | "weak";
  relevance_percentage?: number;
  humanized_source?: string;
}

export interface DimensionGrounding {
  dimension: string;
  evidence_chunks: string[];
  confidence: number;
}

export interface Dimension {
  name: string;
  description: string;
  naac_requirement: string;
  institutional_value?: string | number;
  status: "covered" | "missing" | "partial";
  impact: "critical" | "high" | "medium";
  evidence_count?: number;
}

export interface Gap {
  dimension: string;
  description: string;
  priority: "critical" | "high" | "medium";
  impact: string;
  naac_requirement?: string;
  quickFix?: string;
  estimatedEffort?: "low" | "medium" | "high";
}

export interface Recommendation {
  id: string;
  priority: "critical" | "high" | "medium";
  title: string;
  description: string;
  actionItems: string[];
  expectedImpact: string;
  category: "evidence" | "documentation" | "quality" | "coverage";
  criterionSpecific: boolean;
}

export interface Grade {
  current: string;  // "C", "B", "B+", "A", "A+", "A++"
  target: string;
  color: string;
  description: string;
  confidenceRange: [number, number];
  progressPercentage: number;
}

export interface Theme {
  id: "quiet-night" | "morning-light" | "rainy-afternoon";
  name: string;
  description: string;
  icon: string;
}
