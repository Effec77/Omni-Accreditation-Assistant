"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import { 
  TrendingUp, Target, Lightbulb, ArrowRight, BarChart3, 
  CheckCircle2, AlertCircle, Clock, Award, Users, BookOpen,
  ArrowUpRight, Sparkles, ChevronRight, Calendar
} from "lucide-react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, 
  PolarRadiusAxis, Radar, LineChart, Line, PieChart, Pie, Cell 
} from 'recharts';

function RecommendationsContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [auditData, setAuditData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get audit data from localStorage (passed from main page)
    const storedData = localStorage.getItem('currentAuditResult');
    if (storedData) {
      const parsedData = JSON.parse(storedData);
      console.log('[Recommendations] Loaded audit data:', parsedData);
      console.log('[Recommendations] Grade from data:', parsedData.grade);
      console.log('[Recommendations] Confidence from data:', parsedData.confidence_score);
      setAuditData(parsedData);
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-lg font-medium gradient-text">Loading recommendations...</p>
        </div>
      </div>
    );
  }

  if (!auditData) {
    return (
      <div className="flex h-screen bg-background">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <AlertCircle className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-2">No Audit Data Found</h2>
            <p className="text-muted-foreground mb-4">Please run an audit first to see recommendations</p>
            <button 
              onClick={() => router.push('/')}
              className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Always use calculated grade for consistency (ignore API grade)
  const grade = calculateGradeFromConfidence(auditData.confidence_score || 0);
  const confidence = auditData.confidence_score || 0;
  const coverage = auditData.coverage_ratio || 0;
  const criterion = auditData.criterion || '3.2.1';
  const framework = auditData.framework || 'NAAC';
  const missingDims = auditData.dimensions_missing || [];
  const coveredDims = auditData.dimensions_covered || [];

  console.log('[Recommendations] Final grade used:', grade);
  console.log('[Recommendations] Confidence used:', confidence);
  console.log('[Recommendations] API Grade:', auditData.grade, 'Calculated Grade:', calculateGradeFromConfidence(confidence));

  // Helper function to calculate grade from confidence (matching frontend logic)
  function calculateGradeFromConfidence(confidence: number): string {
    if (confidence >= 0.85) return 'A+';
    if (confidence >= 0.70) return 'A';
    if (confidence >= 0.50) return 'B+';
    if (confidence >= 0.30) return 'B';
    return 'C';
  }

  // Calculate target grade
  const gradeProgression: Record<string, string> = {
    'C': 'B', 'B': 'B+', 'B+': 'A', 'A': 'A+', 'A+': 'A+'
  };
  const targetGrade = gradeProgression[grade] || 'A+';

  // Calculate target scores
  const getTargetScore = (grade: string): number => {
    if (grade === 'A+') return 85;
    if (grade === 'A') return 70;
    if (grade === 'B+') return 50;
    if (grade === 'B') return 30;
    return 30;
  };
  
  const targetScore = getTargetScore(targetGrade);
  const currentScore = confidence * 100;
  const improvementNeeded = targetScore - currentScore;

  // Performance comparison data
  const performanceData = [
    { category: 'Your Institution', score: currentScore },
    { category: `${targetGrade} Benchmark`, score: targetScore },
    { category: 'Top 10% Institutions', score: 90 },
  ];

  // Dimension coverage radar data
  const radarData = [
    { dimension: 'Funding Amount', current: coveredDims.includes('funding_amount') ? 100 : 0, target: 100 },
    { dimension: 'Project Count', current: coveredDims.includes('project_count') ? 100 : 0, target: 100 },
    { dimension: 'Agencies', current: coveredDims.includes('funding_agencies') ? 100 : 0, target: 100 },
    { dimension: 'Time Period', current: coveredDims.includes('time_period') ? 100 : 0, target: 100 },
    { dimension: 'Documentation', current: confidence * 100, target: 100 },
  ];

  // Timeline milestones with detailed actions
  const timelineData = [
    { 
      month: 'Month 1-2', 
      task: 'Data Collection & Gap Analysis', 
      status: 'pending',
      description: 'Identify and collect all missing data',
      actions: [
        'Audit current documentation to identify gaps',
        'Collect funding data from finance department',
        'Gather project details from faculty and departments',
        'Compile agency-wise funding information',
        'Create master spreadsheet of all research projects'
      ]
    },
    { 
      month: 'Month 3-4', 
      task: 'Systematic Documentation', 
      status: 'pending',
      description: 'Organize and structure all collected data',
      actions: [
        'Create year-wise tables (last 5 years)',
        'Prepare agency-wise breakdown tables',
        'Document project outcomes and impact',
        'Organize supporting documents (sanction letters, certificates)',
        'Draft comprehensive criterion-specific reports'
      ]
    },
    { 
      month: 'Month 5-6', 
      task: 'Verification & Quality Check', 
      status: 'pending',
      description: 'Ensure accuracy and completeness',
      actions: [
        'Cross-verify all data with source documents',
        'Internal peer review of documentation',
        'Ensure all claims are backed by evidence',
        'Check for consistency across documents',
        'Address any discrepancies or missing information'
      ]
    },
    { 
      month: 'Month 7-9', 
      task: 'Enhancement & Improvement', 
      status: 'pending',
      description: 'Strengthen weak areas and add value',
      actions: [
        'Add detailed analysis and context to data',
        'Include impact metrics and outcomes',
        'Enhance visual presentation with charts/graphs',
        'Add case studies of significant projects',
        'Prepare comparative analysis with benchmarks'
      ]
    },
    { 
      month: 'Month 10-12', 
      task: 'Final Review & Submission Prep', 
      status: 'pending',
      description: 'Polish and prepare for assessment',
      actions: [
        'Comprehensive review by NAAC cell',
        'External expert review (if possible)',
        'Final formatting and presentation',
        'Prepare digital repository of all evidence',
        'Mock assessment and readiness check'
      ]
    },
  ];

  // Gap distribution
  const gapData = [
    { name: 'Covered', value: coveredDims.length, color: '#10b981' },
    { name: 'Missing', value: missingDims.length, color: '#ef4444' },
  ];

  const COLORS = ['#10b981', '#ef4444'];

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-border/50 bg-card/50">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold gradient-text mb-2">
                Comprehensive Improvement Roadmap
              </h1>
              <p className="text-muted-foreground">
                {framework} Criterion {criterion} • Current Grade: <span className="text-primary font-bold">{grade}</span> → Target: <span className="text-green-400 font-bold">{targetGrade}</span>
              </p>
            </div>
            <button
              onClick={() => router.push('/')}
              className="px-4 py-2 bg-background border border-border rounded-lg hover:bg-accent"
            >
              ← Back to Dashboard
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            
            {/* Performance Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="glass-card p-6 rounded-xl">
                <div className="flex items-center gap-3 mb-2">
                  <Award className="text-primary" size={24} />
                  <h3 className="font-bold">Current Grade</h3>
                </div>
                <p className="text-4xl font-bold text-primary">{grade}</p>
                <p className="text-sm text-muted-foreground mt-1">Confidence: {(confidence * 100).toFixed(1)}%</p>
              </div>
              
              <div className="glass-card p-6 rounded-xl">
                <div className="flex items-center gap-3 mb-2">
                  <Target className="text-green-400" size={24} />
                  <h3 className="font-bold">Target Grade</h3>
                </div>
                <p className="text-4xl font-bold text-green-400">{targetGrade}</p>
                <p className="text-sm text-muted-foreground mt-1">Gap: {((0.80 - confidence) * 100).toFixed(0)}% improvement needed</p>
              </div>
              
              <div className="glass-card p-6 rounded-xl">
                <div className="flex items-center gap-3 mb-2">
                  <Clock className="text-yellow-400" size={24} />
                  <h3 className="font-bold">Timeline</h3>
                </div>
                <p className="text-4xl font-bold text-yellow-400">9-12</p>
                <p className="text-sm text-muted-foreground mt-1">Months for {targetGrade} grade</p>
              </div>
            </div>

            {/* Performance Comparison Chart */}
            <div className="glass-card p-6 rounded-xl">
              <div className="mb-4">
                <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                  <BarChart3 className="text-primary" />
                  Performance Comparison
                </h3>
                <p className="text-sm text-muted-foreground">
                  This chart compares your institution's current performance against the target benchmark and top-performing institutions. 
                  Your score of {currentScore.toFixed(1)}% needs to reach {targetScore}% 
                  to achieve {targetGrade} grade. The gap of {improvementNeeded.toFixed(0)}% 
                  represents the improvement needed in evidence quality and documentation completeness.
                </p>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                  <XAxis dataKey="category" stroke="#888" />
                  <YAxis stroke="#888" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Bar dataKey="score" fill="#06b6d4" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-4 p-4 bg-primary/10 rounded-lg border border-primary/30">
                <p className="text-sm font-medium mb-2">💡 What this means for you:</p>
                <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                  <li>You need to improve by {improvementNeeded.toFixed(0)}% to reach {targetGrade} grade</li>
                  <li>Focus on adding quantitative data, supporting documents, and year-wise breakdowns</li>
                  <li>Top institutions maintain 90%+ scores through systematic documentation</li>
                </ul>
              </div>
            </div>

            {/* Dimension Coverage Radar */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-card p-6 rounded-xl">
                <div className="mb-4">
                  <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                    <Target className="text-primary" />
                    Dimension Coverage Analysis
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    This radar chart shows how well you've covered each required dimension. The cyan area represents your current coverage, 
                    while the green outline shows the target (100% for all dimensions). Gaps between cyan and green indicate areas needing improvement.
                  </p>
                </div>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#333" />
                    <PolarAngleAxis dataKey="dimension" stroke="#888" />
                    <PolarRadiusAxis stroke="#888" />
                    <Radar name="Current" dataKey="current" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.6} />
                    <Radar name="Target" dataKey="target" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
                <div className="mt-4 p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/30">
                  <p className="text-sm font-medium mb-2">📊 Key Insights:</p>
                  <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                    {missingDims.length > 0 ? (
                      <li className="text-red-400">Missing: {missingDims.join(', ')} - Add these immediately</li>
                    ) : (
                      <li className="text-green-400">All dimensions covered - Focus on quality improvement</li>
                    )}
                    <li>Documentation quality at {(confidence * 100).toFixed(0)}% - Target: 100%</li>
                  </ul>
                </div>
              </div>

              <div className="glass-card p-6 rounded-xl">
                <div className="mb-4">
                  <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                    <AlertCircle className="text-yellow-400" />
                    Gap Distribution
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    This pie chart visualizes the proportion of dimensions you've covered (green) versus those still missing (red). 
                    For {targetGrade} grade, you need 100% coverage (all green) with high-quality evidence for each dimension.
                  </p>
                </div>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={gapData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}`}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {gapData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <div className="mt-4 space-y-2">
                  <div className="flex items-center justify-between p-2 bg-green-500/10 rounded">
                    <span className="text-sm">✅ Dimensions Covered:</span>
                    <span className="font-bold text-green-400">{coveredDims.length}</span>
                  </div>
                  <div className="flex items-center justify-between p-2 bg-red-500/10 rounded">
                    <span className="text-sm">❌ Dimensions Missing:</span>
                    <span className="font-bold text-red-400">{missingDims.length}</span>
                  </div>
                  {missingDims.length > 0 && (
                    <div className="p-3 bg-red-500/10 rounded-lg border border-red-500/30 mt-2">
                      <p className="text-sm font-medium text-red-400 mb-1">Action Required:</p>
                      <p className="text-xs text-muted-foreground">
                        Add {missingDims.join(', ')} to your documentation immediately. These are blocking your progress to {targetGrade}.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Action Plan Timeline */}
            <div className="glass-card p-6 rounded-xl">
              <div className="mb-6">
                <h3 className="text-xl font-bold mb-2 flex items-center gap-2">
                  <Calendar className="text-primary" />
                  12-Month Action Plan Timeline
                </h3>
                <p className="text-sm text-muted-foreground">
                  This roadmap breaks down your journey to {targetGrade} grade into 5 phases over 12 months. 
                  Each phase has specific objectives and action items. Click on any phase to see detailed steps.
                </p>
              </div>
              <div className="space-y-6">
                {timelineData.map((milestone, idx) => (
                  <details key={idx} className="group">
                    <summary className="cursor-pointer list-none">
                      <div className="flex items-start gap-4 p-4 bg-background/50 rounded-lg border border-border hover:border-primary/50 transition-all">
                        <div className="flex-shrink-0 w-24 pt-1">
                          <span className="text-sm font-bold text-primary">{milestone.month}</span>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <div className="w-3 h-3 rounded-full bg-primary"></div>
                            <h4 className="font-bold text-lg">{milestone.task}</h4>
                            <ChevronRight className="ml-auto text-muted-foreground group-open:rotate-90 transition-transform" size={20} />
                          </div>
                          <p className="text-sm text-muted-foreground">{milestone.description}</p>
                        </div>
                      </div>
                    </summary>
                    <div className="mt-2 ml-28 p-4 bg-primary/5 rounded-lg border-l-4 border-primary">
                      <p className="text-sm font-medium mb-3 text-primary">Detailed Action Items:</p>
                      <ul className="space-y-2">
                        {milestone.actions.map((action, actionIdx) => (
                          <li key={actionIdx} className="flex items-start gap-3">
                            <CheckCircle2 size={16} className="text-green-400 flex-shrink-0 mt-0.5" />
                            <span className="text-sm text-foreground">{action}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </details>
                ))}
              </div>
              <div className="mt-6 p-4 bg-gradient-to-r from-primary/10 to-accent/10 rounded-lg border border-primary/30">
                <p className="text-sm font-medium mb-2">⏱️ Timeline Tips:</p>
                <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
                  <li>Start immediately with Month 1-2 activities - data collection is critical</li>
                  <li>Phases can overlap - begin documentation while still collecting data</li>
                  <li>Set monthly review meetings to track progress</li>
                  <li>Adjust timeline based on your institution's capacity and resources</li>
                </ul>
              </div>
            </div>

            {/* Detailed Recommendations */}
            <div className="glass-card p-6 rounded-xl">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                <Lightbulb className="text-yellow-400" />
                Detailed Action Items
              </h3>
              
              <div className="space-y-6">
                {/* Critical Actions */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-sm font-bold">
                      CRITICAL
                    </div>
                    <h4 className="font-bold text-lg">Immediate Actions (Month 1-3)</h4>
                  </div>
                  <div className="space-y-3">
                    {missingDims.length > 0 && (
                      <div className="p-4 bg-background/50 rounded-lg border border-red-500/30">
                        <div className="flex items-start gap-3">
                          <AlertCircle className="text-red-400 flex-shrink-0 mt-1" size={20} />
                          <div className="flex-1">
                            <p className="font-medium mb-2">Add Missing Dimensions: {missingDims.join(', ')}</p>
                            <p className="text-sm text-muted-foreground">These are blocking your progress to {targetGrade}. Collect and document this data immediately.</p>
                          </div>
                        </div>
                      </div>
                    )}
                    {confidence < 0.7 && (
                      <div className="p-4 bg-background/50 rounded-lg border border-red-500/30">
                        <div className="flex items-start gap-3">
                          <AlertCircle className="text-red-400 flex-shrink-0 mt-1" size={20} />
                          <div className="flex-1">
                            <p className="font-medium mb-2">Strengthen Evidence Quality</p>
                            <p className="text-sm text-muted-foreground">Current confidence is {(confidence*100).toFixed(1)}%. Need {((0.80-confidence)*100).toFixed(0)}% improvement. Add specific numbers, dates, and supporting documents.</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* High Priority Actions */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="px-3 py-1 bg-orange-500/20 text-orange-400 rounded-full text-sm font-bold">
                      HIGH PRIORITY
                    </div>
                    <h4 className="font-bold text-lg">Short-term Actions (Month 4-6)</h4>
                  </div>
                  <div className="space-y-3">
                    <div className="p-4 bg-background/50 rounded-lg border border-orange-500/30">
                      <div className="flex items-start gap-3">
                        <CheckCircle2 className="text-orange-400 flex-shrink-0 mt-1" size={20} />
                        <div className="flex-1">
                          <p className="font-medium mb-2">Systematic Documentation</p>
                          <p className="text-sm text-muted-foreground">Create year-wise tables for last 5 years. Include agency-wise breakdown, project details, and funding amounts.</p>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-background/50 rounded-lg border border-orange-500/30">
                      <div className="flex items-start gap-3">
                        <CheckCircle2 className="text-orange-400 flex-shrink-0 mt-1" size={20} />
                        <div className="flex-1">
                          <p className="font-medium mb-2">Collect Supporting Documents</p>
                          <p className="text-sm text-muted-foreground">Gather sanction letters, completion reports, utilization certificates, and project outcomes.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Medium Priority Actions */}
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="px-3 py-1 bg-yellow-500/20 text-yellow-400 rounded-full text-sm font-bold">
                      MEDIUM PRIORITY
                    </div>
                    <h4 className="font-bold text-lg">Long-term Strategy (Month 7-12)</h4>
                  </div>
                  <div className="space-y-3">
                    <div className="p-4 bg-background/50 rounded-lg border border-yellow-500/30">
                      <div className="flex items-start gap-3">
                        <Users className="text-yellow-400 flex-shrink-0 mt-1" size={20} />
                        <div className="flex-1">
                          <p className="font-medium mb-2">Establish NAAC Cell</p>
                          <p className="text-sm text-muted-foreground">Set up dedicated team for continuous documentation and quality assurance.</p>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-background/50 rounded-lg border border-yellow-500/30">
                      <div className="flex items-start gap-3">
                        <BookOpen className="text-yellow-400 flex-shrink-0 mt-1" size={20} />
                        <div className="flex-1">
                          <p className="font-medium mb-2">Faculty Training Programs</p>
                          <p className="text-sm text-muted-foreground">Organize workshops on research proposal writing, funding acquisition, and documentation standards.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Benchmarking */}
            <div className="glass-card p-6 rounded-xl">
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <TrendingUp className="text-green-400" />
                What Top {targetGrade} Institutions Do Differently
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-background/50 rounded-lg border border-green-500/30">
                  <h4 className="font-bold mb-2 text-green-400">Research Funding</h4>
                  <p className="text-sm text-muted-foreground">Top institutions secure ₹75+ Lakhs annually from multiple agencies (DST, SERB, DBT, Industry).</p>
                </div>
                <div className="p-4 bg-background/50 rounded-lg border border-green-500/30">
                  <h4 className="font-bold mb-2 text-green-400">Documentation Quality</h4>
                  <p className="text-sm text-muted-foreground">Maintain comprehensive digital repositories with year-wise data, supporting documents, and impact metrics.</p>
                </div>
                <div className="p-4 bg-background/50 rounded-lg border border-green-500/30">
                  <h4 className="font-bold mb-2 text-green-400">Continuous Improvement</h4>
                  <p className="text-sm text-muted-foreground">Regular internal audits, faculty training, and systematic tracking of all activities.</p>
                </div>
                <div className="p-4 bg-background/50 rounded-lg border border-green-500/30">
                  <h4 className="font-bold mb-2 text-green-400">Industry Partnerships</h4>
                  <p className="text-sm text-muted-foreground">Strong collaborations with industry for funded research, internships, and knowledge transfer.</p>
                </div>
              </div>
            </div>

            {/* Call to Action */}
            <div className="glass-card p-8 rounded-xl border-2 border-primary/50 bg-gradient-to-br from-primary/10 to-accent/10">
              <div className="flex items-start gap-4">
                <div className="p-3 rounded-lg bg-primary/20">
                  <Sparkles className="text-primary" size={32} />
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold mb-3">Ready to Start Your Journey to {targetGrade}?</h3>
                  <p className="text-muted-foreground mb-6">
                    Follow this roadmap systematically. Start with Critical actions, then move to High Priority items. 
                    Regular monitoring and documentation will help you achieve {targetGrade} grade in 9-12 months.
                  </p>
                  <div className="flex gap-4">
                    <button 
                      onClick={() => router.push('/')}
                      className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 flex items-center gap-2"
                    >
                      Run Another Audit
                      <ArrowRight size={20} />
                    </button>
                    <button 
                      onClick={() => window.print()}
                      className="px-6 py-3 bg-background border border-border rounded-lg hover:bg-accent"
                    >
                      Download Report
                    </button>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

export default function RecommendationsPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center h-screen bg-background">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-lg font-medium gradient-text">Loading recommendations...</p>
        </div>
      </div>
    }>
      <RecommendationsContent />
    </Suspense>
  );
}
