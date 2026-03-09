/**
 * Evidence Transformer Utility
 * Converts technical evidence fields into human-readable format
 */

export interface TransformedEvidence {
  content: string;
  relevance: string;
  source: string;
  page: string | null;
  strength: "strong" | "moderate" | "weak";
  strengthLabel: string;
  technicalDetails: {
    rerankerScore: number;
    metadata: Record<string, any>;
    rawSource: string;
  };
}

/**
 * Transform reranker score to human-readable relevance
 */
export function transformRerankerScore(score: number): string {
  const percentage = Math.round(score * 100);
  return `${percentage}% relevant`;
}

/**
 * Determine evidence strength from reranker score
 */
export function getEvidenceStrength(score: number): {
  strength: "strong" | "moderate" | "weak";
  label: string;
} {
  if (score >= 0.7) {
    return { strength: "strong", label: "Strong Evidence" };
  } else if (score >= 0.4) {
    return { strength: "moderate", label: "Moderate Evidence" };
  } else {
    return { strength: "weak", label: "Weak Evidence" };
  }
}

/**
 * Transform metadata into readable format
 */
export function transformMetadata(metadata: Record<string, any>): Record<string, string> {
  const transformed: Record<string, string> = {};
  
  // Common metadata field transformations
  const fieldMap: Record<string, string> = {
    page: "Page",
    section: "Section",
    chapter: "Chapter",
    document_type: "Document Type",
    date: "Date",
    author: "Author"
  };
  
  for (const [key, value] of Object.entries(metadata)) {
    const readableKey = fieldMap[key] || key
      .split("_")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
    
    transformed[readableKey] = String(value);
  }
  
  return transformed;
}

/**
 * Transform source path to readable document name
 */
export function transformSource(source: string): string {
  // Extract filename from path
  const filename = source.split("/").pop() || source;
  
  // Remove file extension
  const nameWithoutExt = filename.replace(/\.[^/.]+$/, "");
  
  // Replace underscores and hyphens with spaces
  const readable = nameWithoutExt
    .replace(/[_-]/g, " ")
    .split(" ")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
  
  return readable;
}

/**
 * Extract page number from metadata or source
 */
export function extractPageNumber(metadata: Record<string, any>): string | null {
  if (metadata.page) {
    return `Page ${metadata.page}`;
  }
  
  if (metadata.page_number) {
    return `Page ${metadata.page_number}`;
  }
  
  return null;
}

/**
 * Transform complete evidence object
 */
export function transformEvidence(evidence: {
  child_text: string;
  reranker_score: number;
  metadata: Record<string, any>;
  source: string;
}): TransformedEvidence {
  const strengthInfo = getEvidenceStrength(evidence.reranker_score);
  
  return {
    content: evidence.child_text,
    relevance: transformRerankerScore(evidence.reranker_score),
    source: transformSource(evidence.source),
    page: extractPageNumber(evidence.metadata),
    strength: strengthInfo.strength,
    strengthLabel: strengthInfo.label,
    technicalDetails: {
      rerankerScore: evidence.reranker_score,
      metadata: evidence.metadata,
      rawSource: evidence.source
    }
  };
}

/**
 * Sort evidence by strength (strong first, weak last)
 */
export function sortEvidenceByStrength(
  evidence: Array<{ reranker_score: number }>
): Array<{ reranker_score: number }> {
  return [...evidence].sort((a, b) => b.reranker_score - a.reranker_score);
}
