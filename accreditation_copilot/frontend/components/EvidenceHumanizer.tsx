"use client";

import { useState } from "react";
import { transformEvidence } from "@/utils/evidenceTransformer";
import { getStrengthColor, getStrengthBgColor } from "@/utils/colorMapper";
import { CheckCircle, AlertCircle, AlertTriangle, ChevronDown, ChevronUp, FileText, MapPin } from "lucide-react";

interface EvidenceHumanizerProps {
  evidence: {
    child_text: string;
    reranker_score: number;
    metadata: Record<string, any>;
    source: string;
  };
  showTechnicalDetails?: boolean;
}

export default function EvidenceHumanizer({ 
  evidence, 
  showTechnicalDetails = false 
}: EvidenceHumanizerProps) {
  const [showDetails, setShowDetails] = useState(showTechnicalDetails);
  const transformed = transformEvidence(evidence);

  // Get strength icon
  const StrengthIcon = 
    transformed.strength === "strong" ? CheckCircle :
    transformed.strength === "moderate" ? AlertTriangle :
    AlertCircle;

  const strengthColor = getStrengthColor(transformed.strength);
  const strengthBgColor = getStrengthBgColor(transformed.strength);

  return (
    <div className="glass-card p-4 rounded-xl space-y-3">
      {/* Strength Badge */}
      <div className="flex items-center justify-between">
        <div className={`flex items-center gap-2 px-3 py-1.5 ${strengthBgColor} rounded-lg`}>
          <StrengthIcon size={16} className={strengthColor} />
          <span className={`text-sm font-medium ${strengthColor}`}>
            {transformed.strengthLabel}
          </span>
        </div>
        <span className="text-sm text-muted-foreground">
          {transformed.relevance}
        </span>
      </div>

      {/* Main Content */}
      <div className="space-y-2">
        <p className="text-foreground leading-relaxed">
          {transformed.content}
        </p>
      </div>

      {/* Source Information */}
      <div className="flex items-center gap-4 text-sm text-muted-foreground pt-2 border-t border-border/50">
        <div className="flex items-center gap-1.5">
          <FileText size={14} />
          <span>{transformed.source}</span>
        </div>
        {transformed.page && (
          <div className="flex items-center gap-1.5">
            <MapPin size={14} />
            <span>{transformed.page}</span>
          </div>
        )}
      </div>

      {/* Technical Details (Collapsible) */}
      <div className="pt-2 border-t border-border/50">
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          {showDetails ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          <span>Technical Details</span>
        </button>

        {showDetails && (
          <div className="mt-3 space-y-2 text-xs">
            <div className="grid grid-cols-2 gap-2">
              <div className="glass-card p-2 rounded-lg">
                <span className="text-muted-foreground">Reranker Score</span>
                <p className="font-mono mt-1">
                  {transformed.technicalDetails.rerankerScore.toFixed(4)}
                </p>
              </div>
              <div className="glass-card p-2 rounded-lg">
                <span className="text-muted-foreground">Raw Source</span>
                <p className="font-mono mt-1 truncate" title={transformed.technicalDetails.rawSource}>
                  {transformed.technicalDetails.rawSource}
                </p>
              </div>
            </div>

            {Object.keys(transformed.technicalDetails.metadata).length > 0 && (
              <div className="glass-card p-2 rounded-lg">
                <span className="text-muted-foreground">Metadata</span>
                <div className="mt-1 space-y-1">
                  {Object.entries(transformed.technicalDetails.metadata).map(([key, value]) => (
                    <div key={key} className="flex justify-between">
                      <span className="text-muted-foreground">{key}:</span>
                      <span className="font-mono">{String(value)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
