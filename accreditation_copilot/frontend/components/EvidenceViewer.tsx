"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { FileText, Filter, Table, List } from "lucide-react";
import EvidenceHumanizer from "./EvidenceHumanizer";
import EvidenceTableVisualizer from "./EvidenceTableVisualizer";
import { sortEvidenceByStrength } from "@/utils/evidenceTransformer";

interface EvidenceViewerProps {
  evidence: any[];
  dimensions?: string[];
}

interface EvidenceItem {
  text?: string;
  child_text?: string;
  reranker_score?: number;
  source?: string;
  metadata?: Record<string, any>;
}

export default function EvidenceViewer({ evidence, dimensions = [] }: EvidenceViewerProps) {
  const [strengthFilter, setStrengthFilter] = useState<"all" | "strong" | "moderate" | "weak">("all");
  const [viewMode, setViewMode] = useState<'structured' | 'list'>('structured');
  
  // Sort evidence by strength (strong first)
  const sortedEvidence = sortEvidenceByStrength(evidence || []) as EvidenceItem[];
  
  // Filter evidence by strength
  const filteredEvidence = strengthFilter === "all" 
    ? sortedEvidence
    : sortedEvidence.filter(item => {
        const score = item.reranker_score || 0;
        if (strengthFilter === "strong") return score >= 0.7;
        if (strengthFilter === "moderate") return score >= 0.4 && score < 0.7;
        if (strengthFilter === "weak") return score < 0.4;
        return true;
      });

  return (
    <div className="space-y-6">
      {/* Header with Filter */}
      <div className="glass-card p-6 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-2xl font-bold">Evidence</h3>
            <p className="text-sm text-muted-foreground mt-1">
              {filteredEvidence.length} of {sortedEvidence.length} evidence chunks
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            {/* View Mode Toggle */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setViewMode('structured')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  viewMode === 'structured'
                    ? 'bg-accent text-accent-foreground'
                    : 'glass-card text-muted-foreground hover:text-foreground'
                }`}
              >
                <Table size={16} className="inline mr-1" />
                Structured
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  viewMode === 'list'
                    ? 'bg-accent text-accent-foreground'
                    : 'glass-card text-muted-foreground hover:text-foreground'
                }`}
              >
                <List size={16} className="inline mr-1" />
                List
              </button>
            </div>
            
            {/* Strength Filter */}
            <div className="flex items-center gap-2">
              <Filter size={16} className="text-muted-foreground" />
              <select
                value={strengthFilter}
                onChange={(e) => setStrengthFilter(e.target.value as any)}
                className="glass-card px-3 py-2 rounded-lg text-sm border border-border/50 focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                <option value="all">All Evidence</option>
                <option value="strong">Strong Only</option>
                <option value="moderate">Moderate Only</option>
                <option value="weak">Weak Only</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      
      {/* Evidence Display */}
      {filteredEvidence && filteredEvidence.length > 0 ? (
        viewMode === 'structured' ? (
          <EvidenceTableVisualizer 
            evidence={filteredEvidence.map(item => ({
              child_text: item.text || item.child_text || 'No text available',
              reranker_score: item.reranker_score || 0,
              source: item.source || 'Unknown Source',
              metadata: item.metadata || {}
            }))}
            dimensions={dimensions}
          />
        ) : (
          <div className="space-y-4">
            {filteredEvidence.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <EvidenceHumanizer 
                  evidence={{
                    child_text: item.text || item.child_text || 'No text available',
                    reranker_score: item.reranker_score || 0,
                    metadata: item.metadata || {},
                    source: item.source || 'Unknown Source'
                  }}
                  showTechnicalDetails={false}
                />
              </motion.div>
            ))}
          </div>
        )
      ) : (
        <div className="glass-card p-12 rounded-xl text-center">
          <FileText size={48} className="mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">
            {strengthFilter === "all" 
              ? "No evidence found" 
              : `No ${strengthFilter} evidence found`
            }
          </p>
        </div>
      )}
    </div>
  );
}
