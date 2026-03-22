"use client";

import { motion } from "framer-motion";
import { Award, TrendingUp, CheckCircle2, AlertCircle, Target } from "lucide-react";

interface FullAuditDashboardProps {
  result: any;
}

export default function FullAuditDashboard({ result }: FullAuditDashboardProps) {
  const overall = result.overall_result;
  const summary = result.summary;
  const breakdown = overall.breakdown || [];

  const getGradeColor = (grade: string) => {
    if (grade.startsWith('A')) return 'text-green-500';
    if (grade.startsWith('B')) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getGradeBgColor = (grade: string) => {
    if (grade.startsWith('A')) return 'bg-green-500/20 border-green-500/50';
    if (grade.startsWith('B')) return 'bg-yellow-500/20 border-yellow-500/50';
    return 'bg-red-500/20 border-red-500/50';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Overall NAAC Grade Card */}
      <div className="glass-card p-8 rounded-2xl border-2 border-primary/50 bg-gradient-to-br from-primary/10 to-accent/10">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="p-4 rounded-full bg-primary/30 animate-pulse">
              <Award className="text-primary" size={40} />
            </div>
            <div>
              <h2 className="text-3xl font-bold gradient-text">Overall NAAC Grade</h2>
              <p className="text-muted-foreground">Comprehensive Accreditation Assessment</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* CGPA */}
          <div className={`p-6 rounded-xl border-2 ${getGradeBgColor(overall.letter_grade)}`}>
            <div className="text-sm text-muted-foreground mb-2">CGPA (Cumulative Grade Point Average)</div>
            <div className={`text-5xl font-bold ${getGradeColor(overall.letter_grade)}`}>
              {overall.cgpa}
            </div>
            <div className="text-sm text-muted-foreground mt-2">out of 4.00</div>
          </div>

          {/* Letter Grade */}
          <div className={`p-6 rounded-xl border-2 ${getGradeBgColor(overall.letter_grade)}`}>
            <div className="text-sm text-muted-foreground mb-2">Letter Grade</div>
            <div className={`text-5xl font-bold ${getGradeColor(overall.letter_grade)}`}>
              {overall.letter_grade}
            </div>
            <div className="text-sm text-muted-foreground mt-2">{overall.description}</div>
          </div>

          {/* Accreditation Status */}
          <div className={`p-6 rounded-xl border-2 ${getGradeBgColor(overall.letter_grade)}`}>
            <div className="text-sm text-muted-foreground mb-2">Accreditation Status</div>
            <div className="flex items-center gap-2 mt-4">
              {overall.accreditation_status === 'Accredited' ? (
                <CheckCircle2 className="text-green-500" size={32} />
              ) : (
                <AlertCircle className="text-red-500" size={32} />
              )}
              <span className={`text-2xl font-bold ${overall.accreditation_status === 'Accredited' ? 'text-green-500' : 'text-red-500'}`}>
                {overall.accreditation_status}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-4 rounded-xl">
          <div className="text-sm text-muted-foreground">Total Criteria Evaluated</div>
          <div className="text-3xl font-bold text-cyan-400">{summary.criteria_evaluated}</div>
        </div>
        <div className="glass-card p-4 rounded-xl">
          <div className="text-sm text-muted-foreground">Total Metrics Evaluated</div>
          <div className="text-3xl font-bold text-pink-400">{summary.metrics_evaluated}</div>
        </div>
        <div className="glass-card p-4 rounded-xl">
          <div className="text-sm text-muted-foreground">Framework</div>
          <div className="text-3xl font-bold gradient-text">{result.framework}</div>
        </div>
      </div>

      {/* Improvement Suggestions */}
      {result.improvement_suggestions && result.improvement_suggestions.length > 0 && (
        <div className="glass-card p-6 rounded-xl border-2 border-yellow-500/50 bg-yellow-500/10">
          <div className="flex items-center gap-3 mb-4">
            <Target className="text-yellow-400" size={24} />
            <h3 className="text-xl font-bold text-yellow-400">Improvement Roadmap</h3>
          </div>
          <div className="space-y-3">
            {result.improvement_suggestions.map((suggestion: string, index: number) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-background/50 rounded-lg">
                <TrendingUp className="text-yellow-400 flex-shrink-0 mt-1" size={20} />
                <p className="text-foreground">{suggestion}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Criterion Breakdown */}
      <div className="glass-card p-6 rounded-xl">
        <h3 className="text-2xl font-bold mb-6 gradient-text">Criterion-wise Breakdown</h3>
        <div className="space-y-4">
          {breakdown.map((criterion: any, index: number) => (
            <div key={index} className="p-4 bg-background/50 rounded-lg border border-border/50">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h4 className="text-lg font-bold text-cyan-400">{criterion.criterion}</h4>
                  <p className="text-sm text-muted-foreground">Weight: {criterion.weight} points</p>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${getGradeColor(criterion.grade)}`}>
                    {criterion.grade}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {criterion.average_grade_points.toFixed(2)} / 4.00
                  </div>
                </div>
              </div>
              
              {/* Progress Bar */}
              <div className="w-full bg-background rounded-full h-2 mb-2">
                <div
                  className={`h-2 rounded-full ${criterion.grade.startsWith('A') ? 'bg-green-500' : criterion.grade.startsWith('B') ? 'bg-yellow-500' : 'bg-red-500'}`}
                  style={{ width: `${(criterion.average_grade_points / 4.0) * 100}%` }}
                ></div>
              </div>

              {/* Metrics under this criterion */}
              <div className="mt-3 space-y-2">
                {criterion.metrics.map((metric: any, mIndex: number) => (
                  <div key={mIndex} className="flex items-center justify-between text-sm p-2 bg-background/30 rounded">
                    <span className="text-muted-foreground">{metric.metric}</span>
                    <div className="flex items-center gap-3">
                      <span className="text-foreground">{(metric.confidence * 100).toFixed(0)}% confidence</span>
                      <span className={`font-bold ${getGradeColor(metric.grade)}`}>{metric.grade}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
