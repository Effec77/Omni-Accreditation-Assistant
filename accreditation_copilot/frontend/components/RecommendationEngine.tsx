"use client";

import { generateRecommendations, getTopRecommendations, type Recommendation } from "@/utils/recommendationGenerator";
import { getPriorityColor, getPriorityBgColor } from "@/utils/colorMapper";
import { AlertCircle, CheckSquare, TrendingUp, Lightbulb } from "lucide-react";

interface RecommendationEngineProps {
  confidenceScore: number;
  coverageRatio: number;
  missingDimensions: string[];
  criterionId: string;
  showTopOnly?: boolean;
  topCount?: number;
}

export default function RecommendationEngine({ 
  confidenceScore, 
  coverageRatio, 
  missingDimensions, 
  criterionId,
  showTopOnly = false,
  topCount = 3
}: RecommendationEngineProps) {
  const allRecommendations = generateRecommendations(
    confidenceScore,
    coverageRatio,
    missingDimensions,
    criterionId
  );

  const recommendations = showTopOnly 
    ? getTopRecommendations(allRecommendations, topCount)
    : allRecommendations;

  if (recommendations.length === 0) {
    return (
      <div className="glass-card p-6 rounded-xl">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-green-500/20 rounded-lg">
            <CheckSquare size={24} className="text-green-500" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-green-500">
              Excellent Work!
            </h3>
            <p className="text-sm text-muted-foreground mt-1">
              Your documentation meets all NAAC requirements with strong evidence.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const getPriorityIcon = (priority: Recommendation["priority"]) => {
    switch (priority) {
      case "critical":
        return AlertCircle;
      case "high":
        return TrendingUp;
      case "medium":
        return Lightbulb;
    }
  };

  const getPriorityLabel = (priority: Recommendation["priority"]) => {
    switch (priority) {
      case "critical":
        return "Critical";
      case "high":
        return "High Priority";
      case "medium":
        return "Medium Priority";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-6 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Recommendations</h2>
            <p className="text-sm text-muted-foreground mt-1">
              {showTopOnly 
                ? `Top ${recommendations.length} actions to improve your accreditation readiness`
                : `${recommendations.length} action${recommendations.length > 1 ? 's' : ''} to improve your accreditation readiness`
              }
            </p>
          </div>
          <div className="p-3 bg-primary/20 rounded-lg">
            <Lightbulb size={24} className="text-primary" />
          </div>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="space-y-4">
        {recommendations.map((recommendation) => {
          const PriorityIcon = getPriorityIcon(recommendation.priority);
          const priorityColor = getPriorityColor(recommendation.priority);
          const priorityBg = getPriorityBgColor(recommendation.priority);
          const priorityLabel = getPriorityLabel(recommendation.priority);

          return (
            <div 
              key={recommendation.id}
              className={`glass-card p-6 rounded-xl border ${priorityBg.replace('/20', '/30')}`}
            >
              {/* Header */}
              <div className="flex items-start gap-4">
                <div className={`p-3 ${priorityBg} rounded-lg`}>
                  <PriorityIcon size={24} className={priorityColor} />
                </div>
                
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold">
                      {recommendation.title}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium ${priorityBg} ${priorityColor} rounded-lg`}>
                      {priorityLabel}
                    </span>
                  </div>
                  
                  <p className="text-sm text-muted-foreground">
                    {recommendation.description}
                  </p>
                </div>
              </div>

              {/* Action Items */}
              <div className="mt-4 space-y-3">
                <h4 className="text-sm font-semibold text-foreground">
                  Action Items:
                </h4>
                <ul className="space-y-2">
                  {recommendation.actionItems.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-3">
                      <div className="mt-1">
                        <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                      </div>
                      <span className="text-sm text-foreground flex-1">
                        {item}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Expected Impact */}
              <div className="mt-4 pt-4 border-t border-border/50">
                <div className="flex items-start gap-2">
                  <TrendingUp size={16} className="text-primary mt-0.5" />
                  <div>
                    <span className="text-xs font-medium text-muted-foreground">
                      Expected Impact:
                    </span>
                    <p className="text-sm text-foreground mt-1">
                      {recommendation.expectedImpact}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Show All Link */}
      {showTopOnly && allRecommendations.length > topCount && (
        <div className="glass-card p-4 rounded-xl text-center">
          <p className="text-sm text-muted-foreground">
            Showing {topCount} of {allRecommendations.length} recommendations
          </p>
        </div>
      )}
    </div>
  );
}
