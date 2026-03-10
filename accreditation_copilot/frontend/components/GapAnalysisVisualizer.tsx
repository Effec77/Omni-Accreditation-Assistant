"use client";

import { CheckCircle, XCircle, AlertCircle, Target } from "lucide-react";
import { getCoverageColor } from "@/utils/colorMapper";

interface Gap {
  dimension: string;
  severity: "critical" | "high" | "medium";
  description: string;
  impact: string;
}

interface GapAnalysisVisualizerProps {
  gaps: Gap[];
  coverageRatio: number;
  totalDimensions: number;
  coveredDimensions: string[];
  missingDimensions: string[];
}

export default function GapAnalysisVisualizer({ 
  gaps, 
  coverageRatio, 
  totalDimensions,
  coveredDimensions,
  missingDimensions
}: GapAnalysisVisualizerProps) {
  const completenessScore = Math.round(coverageRatio * 100);
  const coverageColor = getCoverageColor(coverageRatio);

  // Group gaps by priority
  const criticalGaps = gaps.filter(g => g.severity === "critical");
  const highGaps = gaps.filter(g => g.severity === "high");
  const mediumGaps = gaps.filter(g => g.severity === "medium");

  // Get top 3 most impactful gaps for Quick Fix section
  const quickFixGaps = [...criticalGaps, ...highGaps, ...mediumGaps].slice(0, 3);

  return (
    <div className="space-y-6">
      {/* Header with Completeness Score */}
      <div className="glass-card p-6 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Gap Analysis</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Visual overview of coverage and gaps in your documentation
            </p>
          </div>
          <div className="text-right">
            <div className={`text-4xl font-bold ${coverageColor}`}>
              {completenessScore}%
            </div>
            <p className="text-sm text-muted-foreground">Complete</p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-muted-foreground">
              {coveredDimensions.length} of {totalDimensions} dimensions covered
            </span>
            <span className={coverageColor}>
              {missingDimensions.length} missing
            </span>
          </div>
          <div className="relative h-3 bg-background/50 rounded-full overflow-hidden">
            <div
              className={`absolute inset-y-0 left-0 bg-gradient-to-r ${
                coverageRatio === 1.0 ? "from-green-500 to-green-600" :
                coverageRatio >= 0.7 ? "from-yellow-400 to-yellow-500" :
                "from-red-400 to-red-500"
              } rounded-full transition-all duration-500`}
              style={{ width: `${completenessScore}%` }}
            />
          </div>
        </div>
      </div>

      {/* Gap Matrix */}
      <div className="glass-card p-6 rounded-xl">
        <h3 className="text-lg font-semibold mb-4">Dimension Coverage Matrix</h3>
        
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {/* Covered Dimensions */}
          {coveredDimensions.map((dimension, idx) => (
            <div 
              key={`covered-${idx}`}
              className="flex items-center gap-2 p-3 bg-green-500/10 border border-green-500/30 rounded-lg"
            >
              <CheckCircle size={16} className="text-green-500 flex-shrink-0" />
              <span className="text-xs text-foreground truncate" title={dimension}>
                {dimension}
              </span>
            </div>
          ))}
          
          {/* Missing Dimensions */}
          {missingDimensions.map((dimension, idx) => (
            <div 
              key={`missing-${idx}`}
              className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg"
            >
              <XCircle size={16} className="text-red-500 flex-shrink-0" />
              <span className="text-xs text-foreground truncate" title={dimension}>
                {dimension}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Gaps by Priority */}
      {gaps.length > 0 && (
        <div className="space-y-4">
          {/* Critical Gaps */}
          {criticalGaps.length > 0 && (
            <div className="glass-card p-6 rounded-xl border border-red-500/30 bg-red-500/10">
              <div className="flex items-center gap-3 mb-4">
                <AlertCircle size={24} className="text-red-500" />
                <div>
                  <h3 className="text-lg font-semibold text-red-500">
                    Critical Gaps ({criticalGaps.length})
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    Must be addressed immediately
                  </p>
                </div>
              </div>
              <div className="space-y-3">
                {criticalGaps.map((gap, idx) => (
                  <div key={idx} className="glass-card p-4 rounded-lg">
                    <h4 className="font-semibold text-sm">{gap.dimension}</h4>
                    <p className="text-xs text-muted-foreground mt-1">{gap.description}</p>
                    <p className="text-xs text-red-500 mt-2">Impact: {gap.impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* High Priority Gaps */}
          {highGaps.length > 0 && (
            <div className="glass-card p-6 rounded-xl border border-orange-500/30 bg-orange-500/10">
              <div className="flex items-center gap-3 mb-4">
                <AlertCircle size={24} className="text-orange-500" />
                <div>
                  <h3 className="text-lg font-semibold text-orange-500">
                    High Priority Gaps ({highGaps.length})
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    Should be addressed soon
                  </p>
                </div>
              </div>
              <div className="space-y-3">
                {highGaps.map((gap, idx) => (
                  <div key={idx} className="glass-card p-4 rounded-lg">
                    <h4 className="font-semibold text-sm">{gap.dimension}</h4>
                    <p className="text-xs text-muted-foreground mt-1">{gap.description}</p>
                    <p className="text-xs text-orange-500 mt-2">Impact: {gap.impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Medium Priority Gaps */}
          {mediumGaps.length > 0 && (
            <div className="glass-card p-6 rounded-xl border border-yellow-500/30 bg-yellow-500/10">
              <div className="flex items-center gap-3 mb-4">
                <AlertCircle size={24} className="text-yellow-500" />
                <div>
                  <h3 className="text-lg font-semibold text-yellow-500">
                    Medium Priority Gaps ({mediumGaps.length})
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    Can be addressed over time
                  </p>
                </div>
              </div>
              <div className="space-y-3">
                {mediumGaps.map((gap, idx) => (
                  <div key={idx} className="glass-card p-4 rounded-lg">
                    <h4 className="font-semibold text-sm">{gap.dimension}</h4>
                    <p className="text-xs text-muted-foreground mt-1">{gap.description}</p>
                    <p className="text-xs text-yellow-500 mt-2">Impact: {gap.impact}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Quick Fix Section */}
      {quickFixGaps.length > 0 && (
        <div className="glass-card p-6 rounded-xl border border-primary/30">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-primary/20 rounded-lg">
              <Target size={24} className="text-primary" />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Quick Fixes</h3>
              <p className="text-sm text-muted-foreground">
                Top {quickFixGaps.length} most impactful gaps to address first
              </p>
            </div>
          </div>
          <div className="space-y-3">
            {quickFixGaps.map((gap, idx) => (
              <div key={idx} className="glass-card p-4 rounded-lg">
                <div className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs font-bold text-primary">{idx + 1}</span>
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-sm">{gap.dimension}</h4>
                    <p className="text-xs text-muted-foreground mt-1">{gap.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
