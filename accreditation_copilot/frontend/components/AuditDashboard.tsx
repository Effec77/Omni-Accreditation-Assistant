"use client";

import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle, XCircle, Clock, FileText } from "lucide-react";
import GradeCalculator from "./GradeCalculator";
import ConfidenceScoreVisualizer from "./ConfidenceScoreVisualizer";

interface AuditDashboardProps {
  result: any;
}

export default function AuditDashboard({ result }: AuditDashboardProps) {
  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'compliant':
        return <CheckCircle2 className="text-green-500" size={24} />;
      case 'partially_compliant':
        return <AlertCircle className="text-yellow-500" size={24} />;
      case 'non_compliant':
        return <XCircle className="text-red-500" size={24} />;
      default:
        return <Clock className="text-gray-500" size={24} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'compliant':
        return 'text-green-500';
      case 'partially_compliant':
        return 'text-yellow-500';
      case 'non_compliant':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="glass-card p-6 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Audit Results</h2>
            <p className="text-muted-foreground">
              {result.framework} Criterion {result.criterion}
            </p>
          </div>
          {result.cached && (
            <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
              Cached
            </span>
          )}
        </div>
      </div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Grade Calculator */}
        <div className="glass-card p-6 rounded-xl">
          <h3 className="text-lg font-semibold mb-4">Overall Grade</h3>
          <GradeCalculator 
            confidenceScore={result.confidence_score} 
            showDetails={true}
          />
        </div>

        {/* Confidence Score Visualizer */}
        <div className="glass-card p-6 rounded-xl">
          <ConfidenceScoreVisualizer 
            confidenceScore={result.confidence_score}
            showWarning={true}
            showTooltip={true}
          />
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Compliance Status */}
        <div className="glass-card p-4 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            {getStatusIcon(result.compliance_status)}
            <span className="text-sm text-muted-foreground">Status</span>
          </div>
          <p className={`text-lg font-semibold ${getStatusColor(result.compliance_status)}`}>
            {result.compliance_status.replace('_', ' ')}
          </p>
        </div>

        {/* Coverage Ratio */}
        <div className="glass-card p-4 rounded-xl">
          <p className="text-sm text-muted-foreground mb-2">Coverage</p>
          <div className="flex items-end gap-2">
            <p className="text-2xl font-bold">{(result.coverage_ratio * 100).toFixed(0)}%</p>
          </div>
          <div className="w-full bg-background/50 rounded-full h-2 mt-2">
            <div
              className="bg-gradient-to-r from-green-400 to-green-500 h-2 rounded-full transition-all"
              style={{ width: `${result.coverage_ratio * 100}%` }}
            />
          </div>
        </div>

        {/* Evidence Count */}
        <div className="glass-card p-4 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <FileText size={16} className="text-primary" />
            <span className="text-sm text-muted-foreground">Evidence</span>
          </div>
          <p className="text-2xl font-bold">{result.evidence_count}</p>
          <p className="text-sm text-muted-foreground mt-1">chunks found</p>
        </div>
      </div>
    </motion.div>
  );
}
