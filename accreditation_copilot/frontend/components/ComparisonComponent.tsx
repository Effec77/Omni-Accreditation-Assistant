"use client";

import { CheckCircle, XCircle, AlertCircle } from "lucide-react";
import { getCoverageColor } from "@/utils/colorMapper";

interface Dimension {
  name: string;
  naac_requirement: string;
  institutional_value?: string | number;
  status: "covered" | "missing" | "partial";
}

interface ComparisonComponentProps {
  dimensions: Dimension[];
  coverageRatio: number;
}

export default function ComparisonComponent({ 
  dimensions, 
  coverageRatio 
}: ComparisonComponentProps) {
  const coveredDimensions = dimensions.filter(d => d.status === "covered");
  const missingDimensions = dimensions.filter(d => d.status === "missing");
  const partialDimensions = dimensions.filter(d => d.status === "partial");
  
  const coverageColor = getCoverageColor(coverageRatio);

  return (
    <div className="space-y-6">
      {/* Header with Coverage Summary */}
      <div className="glass-card p-6 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">NAAC vs Institutional Comparison</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Comparing NAAC requirements with your institutional evidence
            </p>
          </div>
          <div className="text-right">
            <div className={`text-3xl font-bold ${coverageColor}`}>
              {Math.round(coverageRatio * 100)}%
            </div>
            <p className="text-sm text-muted-foreground">Coverage</p>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div className="glass-card p-4 rounded-lg">
            <div className="flex items-center gap-2">
              <CheckCircle size={20} className="text-green-500" />
              <span className="text-2xl font-bold text-green-500">
                {coveredDimensions.length}
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">Covered</p>
          </div>
          
          <div className="glass-card p-4 rounded-lg">
            <div className="flex items-center gap-2">
              <AlertCircle size={20} className="text-yellow-500" />
              <span className="text-2xl font-bold text-yellow-500">
                {partialDimensions.length}
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">Partial</p>
          </div>
          
          <div className="glass-card p-4 rounded-lg">
            <div className="flex items-center gap-2">
              <XCircle size={20} className="text-red-500" />
              <span className="text-2xl font-bold text-red-500">
                {missingDimensions.length}
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">Missing</p>
          </div>
        </div>
      </div>

      {/* Dimension Comparisons */}
      <div className="space-y-4">
        {dimensions.map((dimension, index) => {
          const StatusIcon = 
            dimension.status === "covered" ? CheckCircle :
            dimension.status === "partial" ? AlertCircle :
            XCircle;
          
          const statusColor = 
            dimension.status === "covered" ? "text-green-500" :
            dimension.status === "partial" ? "text-yellow-500" :
            "text-red-500";
          
          const statusBg = 
            dimension.status === "covered" ? "bg-green-500/10 border-green-500/30" :
            dimension.status === "partial" ? "bg-yellow-500/10 border-yellow-500/30" :
            "bg-red-500/10 border-red-500/30";

          return (
            <div 
              key={index} 
              className={`glass-card p-6 rounded-xl border ${statusBg}`}
            >
              {/* Dimension Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <StatusIcon size={24} className={statusColor} />
                  <div>
                    <h3 className="font-semibold text-lg">{dimension.name}</h3>
                    <span className={`text-sm ${statusColor}`}>
                      {dimension.status.charAt(0).toUpperCase() + dimension.status.slice(1)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Two-Column Comparison */}
              <div className="grid md:grid-cols-2 gap-6">
                {/* NAAC Requirements */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1 h-4 bg-primary rounded-full" />
                    <h4 className="text-sm font-semibold text-primary">
                      NAAC Requirement
                    </h4>
                  </div>
                  <p className="text-sm text-foreground pl-3">
                    {dimension.naac_requirement}
                  </p>
                </div>

                {/* Institutional Evidence */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className={`w-1 h-4 ${statusColor.replace('text-', 'bg-')} rounded-full`} />
                    <h4 className={`text-sm font-semibold ${statusColor}`}>
                      Institutional Evidence
                    </h4>
                  </div>
                  {dimension.institutional_value ? (
                    <p className="text-sm text-foreground pl-3">
                      {dimension.institutional_value}
                    </p>
                  ) : (
                    <p className="text-sm text-muted-foreground italic pl-3">
                      No evidence provided
                    </p>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Missing Dimensions Alert */}
      {missingDimensions.length > 0 && (
        <div className="glass-card p-6 rounded-xl border border-red-500/30 bg-red-500/10">
          <div className="flex items-start gap-3">
            <XCircle size={24} className="text-red-500 mt-1" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-red-500">
                Critical: {missingDimensions.length} Missing Dimension{missingDimensions.length > 1 ? 's' : ''}
              </h3>
              <p className="text-sm text-muted-foreground mt-2">
                The following dimensions are required by NAAC but not covered in your documentation:
              </p>
              <ul className="mt-3 space-y-2">
                {missingDimensions.map((dim, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm">
                    <span className="text-red-500 mt-1">•</span>
                    <span className="text-foreground">{dim.name}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
