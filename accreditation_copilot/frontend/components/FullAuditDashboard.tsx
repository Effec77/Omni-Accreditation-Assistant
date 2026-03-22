"use client";

import { motion } from "framer-motion";
import { Award, TrendingUp, CheckCircle2, AlertCircle, Target, FileText, BarChart3, Shield, CheckCircle } from "lucide-react";

interface FullAuditDashboardProps {
  result: any;
}

export default function FullAuditDashboard({ result }: FullAuditDashboardProps) {
  const overall = result.overall_result;
  const summary = result.summary;
  const breakdown = overall.breakdown || [];

  const getGradeColor = (grade: string) => {
    if (grade.startsWith('A')) return 'text-green-400';
    if (grade.startsWith('B')) return 'text-yellow-400';
    return 'text-pink-400';
  };

  const getGradeBgColor = (grade: string) => {
    if (grade.startsWith('A')) return 'bg-green-500/10 border-green-500/50';
    if (grade.startsWith('B')) return 'bg-yellow-500/10 border-yellow-500/50';
    return 'bg-pink-500/10 border-pink-500/50';
  };

  const getComplianceColor = (grade: string) => {
    if (grade.startsWith('A')) return 'bg-green-500/10 text-green-400';
    if (grade.startsWith('B')) return 'bg-yellow-500/10 text-yellow-400';
    return 'bg-pink-500/10 text-pink-400';
  };

  // Calculate progress percentage for circular ring
  const gradePoints = overall.cgpa;
  const progressPercentage = (gradePoints / 4.0) * 100;
  const circumference = 2 * Math.PI * 110;
  const strokeDashoffset = circumference - (progressPercentage / 100) * circumference;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-12"
    >
      {/* Hero Section: Accreditation Overview */}
      <section>
        <div className="glass-card rounded-3xl p-8 relative overflow-hidden group">
          {/* Animated background blobs */}
          <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary/10 rounded-full blur-3xl group-hover:bg-primary/20 transition-all duration-700"></div>
          <div className="absolute -bottom-24 -left-24 w-80 h-80 bg-secondary/10 rounded-full blur-3xl group-hover:bg-secondary/20 transition-all duration-700"></div>
          
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-12">
            <div className="flex-1 space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-[10px] font-bold uppercase tracking-widest">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
                Status: {overall.accreditation_status}
              </div>
              <h2 className="text-5xl font-bold leading-tight">
                Institutional <br/>
                <span className="gradient-text">Accreditation Hub</span>
              </h2>
              <div className="flex gap-10">
                <div>
                  <p className="text-muted-foreground text-xs uppercase tracking-wider mb-1">Current CGPA Estimate</p>
                  <p className="text-3xl font-bold text-white">{overall.cgpa}</p>
                </div>
                <div className="h-12 w-px bg-white/10"></div>
                <div>
                  <p className="text-muted-foreground text-xs uppercase tracking-wider mb-1">Audit Confidence</p>
                  <p className="text-3xl font-bold text-white">High</p>
                </div>
              </div>
            </div>
            
            {/* Circular Progress Ring */}
            <div className="w-64 h-64 relative flex items-center justify-center">
              <svg className="w-full h-full -rotate-90">
                <circle 
                  className="text-indigo-900/30" 
                  cx="128" 
                  cy="128" 
                  fill="transparent" 
                  r="110" 
                  stroke="currentColor" 
                  strokeWidth="12"
                />
                <circle 
                  className="text-primary drop-shadow-[0_0_8px_rgba(193,255,254,0.6)]" 
                  cx="128" 
                  cy="128" 
                  fill="transparent" 
                  r="110" 
                  stroke="currentColor" 
                  strokeDasharray={circumference}
                  strokeDashoffset={strokeDashoffset}
                  strokeWidth="12"
                  style={{ transition: 'stroke-dashoffset 1s ease' }}
                />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-6xl font-black text-white drop-shadow-[0_0_15px_rgba(193,255,254,0.4)]">
                  {overall.letter_grade}
                </span>
                <span className="text-[10px] font-bold uppercase tracking-widest text-primary/80 mt-1">
                  Letter Grade
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Metrics Bento Grid */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-2xl hover:bg-surface-bright/20 transition-all group">
          <FileText className="text-secondary mb-4" size={24} />
          <p className="text-muted-foreground text-[11px] uppercase tracking-wider mb-1">Evidence Ingested</p>
          <p className="text-2xl font-bold text-white">
            {summary.criteria_evaluated} <span className="text-sm font-normal text-indigo-300/50">docs</span>
          </p>
          <div className="mt-4 w-full bg-white/5 h-1 rounded-full overflow-hidden">
            <div className="bg-secondary h-full w-[90%]"></div>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl hover:bg-surface-bright/20 transition-all group">
          <BarChart3 className="text-cyan-400 mb-4" size={24} />
          <p className="text-muted-foreground text-[11px] uppercase tracking-wider mb-1">Coverage Ratio</p>
          <p className="text-2xl font-bold text-white">85%</p>
          <div className="mt-4 w-full bg-white/5 h-1 rounded-full overflow-hidden">
            <div className="bg-cyan-400 h-full w-[85%]"></div>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl hover:bg-surface-bright/20 transition-all group">
          <Shield className="text-purple-400 mb-4" size={24} />
          <p className="text-muted-foreground text-[11px] uppercase tracking-wider mb-1">Confidence Score</p>
          <p className="text-2xl font-bold text-white">0.856</p>
          <div className="mt-4 w-full bg-white/5 h-1 rounded-full overflow-hidden">
            <div className="bg-purple-400 h-full w-[86%]"></div>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl hover:bg-surface-bright/20 transition-all group">
          <CheckCircle className="text-primary mb-4" size={24} />
          <p className="text-muted-foreground text-[11px] uppercase tracking-wider mb-1">Metrics Evaluated</p>
          <p className="text-2xl font-bold text-white">{summary.metrics_evaluated} / {summary.metrics_evaluated}</p>
          <div className="mt-4 w-full bg-white/5 h-1 rounded-full overflow-hidden">
            <div className="bg-primary h-full w-full"></div>
          </div>
        </div>
      </section>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Criterion Breakdown Table */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold flex items-center gap-2">
              <span className="w-1 h-6 bg-secondary rounded-full"></span>
              Criterion Breakdown
            </h3>
            <button className="text-xs text-primary font-bold hover:underline">View All Criteria</button>
          </div>

          <div className="glass-card rounded-2xl overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead className="bg-white/5 border-b border-white/5">
                <tr>
                  <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-indigo-300/50">Criterion ID</th>
                  <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-indigo-300/50">Domain Description</th>
                  <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-indigo-300/50">Compliance</th>
                  <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-indigo-300/50">Evidence</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {breakdown.slice(0, 4).map((criterion: any, index: number) => (
                  <tr key={index} className="hover:bg-white/[0.02] transition-colors">
                    <td className="px-6 py-4 font-mono text-cyan-300 text-sm">{criterion.criterion}</td>
                    <td className="px-6 py-4 text-sm font-medium">{criterion.criterion}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded-md ${getComplianceColor(criterion.grade)} text-[10px] font-bold uppercase`}>
                        {criterion.grade.startsWith('A') ? 'Compliant' : criterion.grade.startsWith('B') ? 'Partial' : 'Weak'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-indigo-300/70">{criterion.metrics?.length || 0} files</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Gap Analysis */}
          {breakdown.some((c: any) => !c.grade.startsWith('A')) && (
            <div className="glass-card rounded-2xl p-6 border-l-4 border-pink-500 bg-pink-500/5">
              <div className="flex items-start gap-4">
                <AlertCircle className="text-pink-500 mt-1 flex-shrink-0" size={20} />
                <div>
                  <h4 className="font-bold text-white mb-1">Critical Gap Detected</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    System identified areas requiring improvement across multiple criteria. Focus on strengthening documentation and evidence collection.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Roadmap to A+ */}
        <div className="space-y-6">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <span className="w-1 h-6 bg-primary rounded-full"></span>
            Roadmap to A+
          </h3>
          
          {result.improvement_suggestions && result.improvement_suggestions.length > 0 ? (
            <div className="space-y-4">
              {result.improvement_suggestions.slice(0, 3).map((suggestion: string, index: number) => (
                <div key={index} className="glass-card p-5 rounded-2xl relative group hover:scale-[1.02] transition-transform">
                  <div className="flex justify-between items-start mb-3">
                    <span className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-tighter ${
                      index === 0 ? 'bg-pink-500/10 text-pink-500' : 
                      index === 1 ? 'bg-cyan-500/10 text-cyan-400' : 
                      'bg-indigo-500/10 text-indigo-400'
                    }`}>
                      {index === 0 ? 'High' : index === 1 ? 'Medium' : 'Low'} Impact
                    </span>
                    <Target className="text-primary text-sm" size={16} />
                  </div>
                  <h5 className="text-sm font-bold text-white mb-2">
                    {suggestion.split(':')[0] || 'Improvement Action'}
                  </h5>
                  <p className="text-[12px] text-muted-foreground mb-4 line-clamp-2">
                    {suggestion}
                  </p>
                  <button className="w-full py-2 bg-white/5 rounded-lg text-xs font-bold hover:bg-white/10 transition-colors">
                    Execute Action
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="glass-card p-5 rounded-2xl">
              <p className="text-sm text-muted-foreground">No improvement suggestions at this time. Excellent work!</p>
            </div>
          )}
        </div>
      </div>

      {/* Detailed Criterion Breakdown */}
      <div className="glass-card p-6 rounded-xl">
        <h3 className="text-2xl font-bold mb-6 gradient-text">Detailed Criterion Analysis</h3>
        <div className="space-y-4">
          {breakdown.map((criterion: any, index: number) => (
            <div key={index} className="p-4 bg-background/50 rounded-lg border border-border/50 hover:border-primary/30 transition-colors">
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
                  className={`h-2 rounded-full transition-all duration-500 ${
                    criterion.grade.startsWith('A') ? 'bg-green-400' : 
                    criterion.grade.startsWith('B') ? 'bg-yellow-400' : 
                    'bg-pink-400'
                  }`}
                  style={{ width: `${(criterion.average_grade_points / 4.0) * 100}%` }}
                ></div>
              </div>

              {/* Metrics under this criterion */}
              {criterion.metrics && criterion.metrics.length > 0 && (
                <div className="mt-3 space-y-2">
                  {criterion.metrics.map((metric: any, mIndex: number) => (
                    <div key={mIndex} className="flex items-center justify-between text-sm p-2 bg-background/30 rounded hover:bg-background/50 transition-colors">
                      <span className="text-muted-foreground">{metric.metric}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-foreground">{(metric.confidence * 100).toFixed(0)}% confidence</span>
                        <span className={`font-bold ${getGradeColor(metric.grade)}`}>{metric.grade}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
