"use client";

import { calculateGrade, formatConfidenceScore } from "@/utils/gradeCalculator";
import { getConfidenceColor, getConfidenceGradient, getConfidenceBgColor } from "@/utils/colorMapper";
import { AlertTriangle, Info } from "lucide-react";

interface ConfidenceScoreVisualizerProps {
  confidenceScore: number;
  showWarning?: boolean;
  showTooltip?: boolean;
}

export default function ConfidenceScoreVisualizer({ 
  confidenceScore, 
  showWarning = true,
  showTooltip = true
}: ConfidenceScoreVisualizerProps) {
  const gradeResult = calculateGrade(confidenceScore);
  const scoreColor = getConfidenceColor(confidenceScore);
  const gradientClass = getConfidenceGradient(confidenceScore);
  const bgColor = getConfidenceBgColor(confidenceScore);
  const showLowScoreWarning = showWarning && confidenceScore < 0.5;

  return (
    <div className="space-y-4">
      {/* Score Display */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-muted-foreground">
            Confidence Score
          </h3>
          <div className="flex items-baseline gap-2 mt-1">
            <span className={`text-3xl font-bold ${scoreColor}`}>
              {formatConfidenceScore(confidenceScore)}
            </span>
            <span className={`text-sm font-medium ${scoreColor}`}>
              {gradeResult.label}
            </span>
          </div>
        </div>
        
        {showTooltip && (
          <div className={`p-3 ${bgColor} rounded-lg`}>
            <div className="flex items-center gap-2">
              <Info size={16} className={scoreColor} />
              <span className={`text-xs font-medium ${scoreColor}`}>
                Grade: {gradeResult.grade}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="relative h-4 bg-background/50 rounded-full overflow-hidden">
          <div
            className={`absolute inset-y-0 left-0 bg-gradient-to-r ${gradientClass} rounded-full transition-all duration-500`}
            style={{ width: `${confidenceScore * 100}%` }}
          />
        </div>
        
        {/* Scale Labels */}
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>0%</span>
          <span>30%</span>
          <span>50%</span>
          <span>70%</span>
          <span>85%</span>
          <span>100%</span>
        </div>
      </div>

      {/* Contextual Label */}
      <div className={`p-3 ${bgColor} rounded-lg`}>
        <p className="text-sm text-foreground">
          {gradeResult.description}
        </p>
      </div>

      {/* Low Score Warning */}
      {showLowScoreWarning && (
        <div className="glass-card p-4 rounded-xl border border-orange-500/30 bg-orange-500/10">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-orange-500/20 rounded-lg">
              <AlertTriangle size={20} className="text-orange-500" />
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-semibold text-orange-500">
                Action Required
              </h4>
              <p className="text-xs text-muted-foreground mt-1">
                Your confidence score is below 50%. Review the recommendations below to improve your evidence quality and coverage.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tooltip Information */}
      {showTooltip && (
        <div className="glass-card p-3 rounded-lg">
          <div className="flex items-start gap-2">
            <Info size={14} className="text-primary mt-0.5" />
            <p className="text-xs text-muted-foreground">
              Confidence score reflects how well your evidence matches NAAC requirements. 
              Higher scores indicate stronger alignment with accreditation standards.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
