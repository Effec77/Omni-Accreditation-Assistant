"use client";

import { calculateGrade, formatConfidenceScore } from "@/utils/gradeCalculator";
import { getConfidenceColor, getConfidenceGradient } from "@/utils/colorMapper";
import { ArrowUp, TrendingUp } from "lucide-react";

interface GradeCalculatorProps {
  confidenceScore: number;
  showDetails?: boolean;
}

export default function GradeCalculator({ 
  confidenceScore, 
  showDetails = true 
}: GradeCalculatorProps) {
  const gradeResult = calculateGrade(confidenceScore);
  const scoreColor = getConfidenceColor(confidenceScore);
  const gradientClass = getConfidenceGradient(confidenceScore);

  return (
    <div className="space-y-4">
      {/* Grade Badge */}
      <div className="flex items-center gap-4">
        <div className={`text-6xl font-bold ${scoreColor}`}>
          {gradeResult.grade}
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className={`text-2xl font-semibold ${scoreColor}`}>
              {gradeResult.label}
            </span>
            {gradeResult.nextGrade && (
              <div className="flex items-center gap-1 text-sm text-muted-foreground">
                <ArrowUp size={16} />
                <span>to {gradeResult.nextGrade}</span>
              </div>
            )}
          </div>
          <p className="text-sm text-muted-foreground mt-1">
            {gradeResult.description}
          </p>
        </div>
      </div>

      {showDetails && (
        <>
          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">
                Confidence Score
              </span>
              <span className={`font-semibold ${scoreColor}`}>
                {formatConfidenceScore(confidenceScore)}
              </span>
            </div>
            <div className="relative h-3 bg-background/50 rounded-full overflow-hidden">
              <div
                className={`absolute inset-y-0 left-0 bg-gradient-to-r ${gradientClass} rounded-full transition-all duration-500`}
                style={{ width: `${confidenceScore * 100}%` }}
              />
            </div>
          </div>

          {/* Progress Within Grade Range */}
          <div className="glass-card p-4 rounded-xl space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">
                Progress in {gradeResult.grade} Range
              </span>
              <span className="text-sm font-medium">
                {Math.round(gradeResult.progressInRange * 100)}%
              </span>
            </div>
            <div className="relative h-2 bg-background/50 rounded-full overflow-hidden">
              <div
                className={`absolute inset-y-0 left-0 bg-gradient-to-r ${gradientClass} rounded-full transition-all duration-500`}
                style={{ width: `${gradeResult.progressInRange * 100}%` }}
              />
            </div>
          </div>

          {/* Path to Next Grade */}
          {gradeResult.nextGrade && gradeResult.pointsToNextGrade !== null && (
            <div className="glass-card p-4 rounded-xl">
              <div className="flex items-start gap-3">
                <div className="p-2 bg-primary/20 rounded-lg">
                  <TrendingUp size={20} className="text-primary" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium">
                    Path to {gradeResult.nextGrade}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Improve by {formatConfidenceScore(gradeResult.pointsToNextGrade)} to reach the next grade
                  </p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
