"use client";

import { motion } from "framer-motion";
import { Lightbulb, TrendingUp, Target, CheckCircle2, ArrowRight, BarChart3, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";

interface GapAnalysisPanelProps {
  gaps: any[];
  recommendations?: string[];
  result?: any;
}

export default function GapAnalysisPanel({ gaps, recommendations, result }: GapAnalysisPanelProps) {
  const router = useRouter();
  
  // Debug: Log the result to see what we're receiving
  console.log('[GapAnalysisPanel] Received result:', result);
  
  // Helper function to calculate grade from confidence (matching frontend logic)
  const calculateGradeFromConfidence = (confidence: number): string => {
    if (confidence >= 0.85) return 'A+';
    if (confidence >= 0.70) return 'A';
    if (confidence >= 0.50) return 'B+';
    if (confidence >= 0.30) return 'B';
    return 'C';
  };
  
  // Extract grade from result (always use calculated grade for consistency)
  const grade = calculateGradeFromConfidence(result?.confidence_score || 0);
  const confidence = result?.confidence_score || 0;
  const coverage = result?.coverage_ratio || 0;
  
  console.log('[GapAnalysisPanel] Grade:', grade, 'Confidence:', confidence, 'Coverage:', coverage);
  console.log('[GapAnalysisPanel] API Grade:', result?.grade, 'Calculated Grade:', calculateGradeFromConfidence(confidence));
  
  // Function to navigate to detailed recommendations page in new tab
  const viewDetailedRecommendations = () => {
    // Always use calculated grade for consistency
    const calculatedGrade = calculateGradeFromConfidence(result?.confidence_score || 0);
    
    // Enhanced result with calculated grade (override API grade for consistency)
    const enhancedResult = {
      ...result,
      grade: calculatedGrade
    };
    
    console.log('[GapAnalysisPanel] Storing enhanced result with calculated grade:', calculatedGrade);
    
    // Store audit result in localStorage for the recommendations page
    localStorage.setItem('currentAuditResult', JSON.stringify(enhancedResult));
    // Open in new tab
    window.open('/recommendations', '_blank');
  };
  
  // Generate actionable recommendations based on the audit result
  const generateActionableRecommendations = () => {
    const recs = [];
    
    // Check what's covered and what's missing
    const dimensionsCovered = result?.dimensions_covered || [];
    const dimensionsMissing = result?.dimensions_missing || [];
    const confidenceScore = result?.confidence_score || 0;
    const coverageRatio = result?.coverage_ratio || 0;
    
    // Determine target grade
    const gradeProgression: Record<string, string> = {
      'C': 'B', 'B': 'B+', 'B+': 'A', 'A': 'A+', 'A+': 'A+'
    };
    const targetGrade = gradeProgression[grade] || 'A+';
    
    console.log('[GapAnalysisPanel] Dimensions covered:', dimensionsCovered);
    console.log('[GapAnalysisPanel] Dimensions missing:', dimensionsMissing);
    console.log('[GapAnalysisPanel] Target grade:', targetGrade);
    
    // Recommendation 1: Based on confidence score
    if (confidenceScore < 0.7) {
      const improvementNeeded = ((0.75 - confidenceScore) * 100).toFixed(0);
      recs.push({
        title: `Strengthen Evidence Quality (Need +${improvementNeeded}% improvement)`,
        description: `Your current confidence score is ${(confidenceScore*100).toFixed(1)}%. To reach ${targetGrade} grade, you need comprehensive documentation with specific numbers, dates, and verifiable proof.`,
        actions: [
          "Collect detailed quantitative data for all activities (numbers, amounts, dates)",
          "Replace general statements with specific institutional data and metrics",
          "Add supporting documents: sanction letters, completion reports, certificates",
          "Ensure all claims are backed by verifiable evidence with proper documentation",
          "Create year-wise breakdown tables showing trends over 5 years"
        ],
        priority: "Critical",
        impact: `Can improve score by ${improvementNeeded}% to reach ${targetGrade}`
      });
    }
    
    // Recommendation 2: Based on missing dimensions
    if (dimensionsMissing.length > 0) {
      const missingDims = dimensionsMissing.map((d: string) => {
        if (d === 'funding_amount') return 'total research funding amounts';
        if (d === 'project_count') return 'number of funded projects';
        if (d === 'funding_agencies') return 'funding agency details';
        if (d === 'time_period') return 'year-wise breakdown';
        return d;
      }).join(', ');
      
      recs.push({
        title: `Add Missing Critical Data: ${missingDims}`,
        description: `You're missing ${dimensionsMissing.length} key dimension(s) that NAAC requires for ${targetGrade} grade. These must be added to your documentation.`,
        actions: [
          `Provide complete ${missingDims} in your institutional reports`,
          "Create detailed tables with all required data points",
          "Ensure all data is verifiable with supporting documents",
          "Update your Self-Study Report (SSR) with this information",
          "Cross-verify data accuracy before submission"
        ],
        priority: "Critical",
        impact: `Required for ${targetGrade} grade - blocks progression without this`
      });
    }
    
    // Recommendation 3: Based on coverage
    if (coverageRatio < 1.0) {
      const missingCoverage = ((1.0 - coverageRatio) * 100).toFixed(0);
      recs.push({
        title: `Complete Missing Dimensions (${missingCoverage}% incomplete)`,
        description: `You have ${(coverageRatio*100).toFixed(0)}% coverage. ${targetGrade} grade requires 100% coverage of all required dimensions.`,
        actions: [
          `Address the ${dimensionsMissing.length} missing dimension(s) listed above`,
          "Review NAAC criterion requirements to identify gaps",
          "Collect data for all missing dimensions systematically",
          "Ensure institutional data is available for the last 5 years",
          "Maintain continuous documentation going forward"
        ],
        priority: "High",
        impact: `Need ${missingCoverage}% more coverage to reach ${targetGrade}`
      });
    } else if (coverageRatio === 1.0 && confidenceScore < 0.7) {
      recs.push({
        title: "Improve Evidence Quality (All dimensions covered but weak evidence)",
        description: "You have 100% coverage but evidence quality is insufficient. Focus on providing detailed, quantitative, verifiable data.",
        actions: [
          "Replace vague statements with specific numbers and metrics",
          "Add comprehensive tables showing year-wise data for 5 years",
          "Include proof documents: sanction letters, completion certificates, publications",
          "Provide institutional data, not just framework guidelines or templates",
          "Add context and analysis to show impact and outcomes"
        ],
        priority: "High",
        impact: `Can improve from ${grade} to ${targetGrade} with better evidence`
      });
    }
    
    // Recommendation 4: Specific to research funding (3.2.1)
    if (result?.criterion === '3.2.1') {
      const fundingThresholds: Record<string, string> = {
        'A++': '₹100+ Lakhs', 'A+': '₹75+ Lakhs', 'A': '₹50+ Lakhs',
        'B+': '₹30+ Lakhs', 'B': '₹15+ Lakhs', 'C': '₹5+ Lakhs'
      };
      const targetFunding = fundingThresholds[targetGrade] || '₹75+ Lakhs';
      
      recs.push({
        title: `Enhance Research Funding Documentation (Target: ${targetFunding})`,
        description: `For NAAC Criterion 3.2.1, ${targetGrade} grade requires substantial evidence of external research funding (${targetFunding} over 5 years).`,
        actions: [
          `Document total research funding received (target: ${targetFunding} for ${targetGrade})`,
          "List ALL externally funded projects with PI names, departments, and exact amounts",
          "Show funding from multiple agencies (DST, SERB, DBT, ICSSR, ICMR, Industry partners)",
          "Provide year-wise breakdown (last 5 years) showing consistent funding or growth",
          "Include copies of sanction letters, fund transfer documents, and utilization certificates",
          "Add project outcomes: publications, patents, products, societal impact"
        ],
        priority: "Critical",
        impact: `Essential for ${targetGrade} in Criterion 3.2.1`
      });
    }
    
    // Recommendation 5: Grade-specific strategy
    if (grade === 'A+' || grade === 'A++') {
      recs.push({
        title: "Maintain and Enhance Excellence",
        description: `Excellent work! You've achieved ${grade} grade. Focus on maintaining this standard and documenting continuous improvement.`,
        actions: [
          "Continue systematic documentation of all activities",
          "Maintain digital repository of all evidence documents",
          "Regular internal audits to ensure data accuracy",
          "Benchmark against top institutions to identify further improvements",
          "Document best practices and innovations for peer learning"
        ],
        priority: "Medium",
        impact: "Sustain excellence and prepare for next assessment cycle"
      });
    } else {
      recs.push({
        title: `Strategic Roadmap: ${grade} → ${targetGrade}`,
        description: `Systematic approach to improve from ${grade} to ${targetGrade} grade in the next assessment cycle.`,
        actions: [
          "Conduct comprehensive internal audit of all NAAC criteria",
          "Set up dedicated NAAC cell with trained personnel for continuous documentation",
          "Organize faculty training on research proposal writing and funding acquisition",
          "Establish industry partnerships for collaborative research and funding",
          "Create digital repository with version control for all evidence documents",
          "Implement quarterly review process to track progress toward ${targetGrade}"
        ],
        priority: "Medium",
        impact: `Long-term strategy for ${grade} → ${targetGrade} improvement`
      });
    }
    
    return recs;
  };
  const actionableRecommendations = generateActionableRecommendations();
  
  // Determine target grade based on current grade
  const getTargetGrade = (currentGrade: string): string => {
    const gradeMap: Record<string, string> = {
      'C': 'B',
      'B': 'B+',
      'B+': 'A',
      'A': 'A+',
      'A+': 'A+'
    };
    return gradeMap[currentGrade] || 'A+';
  };
  
  const targetGrade = getTargetGrade(grade);
  const roadmapTitle = grade === 'A+' 
    ? 'Maintain Excellence' 
    : `Roadmap: ${grade} → ${targetGrade}`;
  const roadmapDescription = grade === 'A+'
    ? 'Steps to maintain and enhance your A+ grade'
    : `Actionable steps to improve from ${grade} to ${targetGrade} grade`;
  
  console.log('[GapAnalysisPanel] Roadmap:', roadmapTitle, '|', roadmapDescription);
  
  // If no recommendations were generated, show a default message
  if (actionableRecommendations.length === 0) {
    return (
      <div className="bg-card rounded-lg border border-border p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-lg bg-primary/10">
            <TrendingUp className="text-primary" size={24} />
          </div>
          <div>
            <h3 className="text-xl font-bold">{roadmapTitle}</h3>
            <p className="text-sm text-muted-foreground">
              {roadmapDescription}
            </p>
          </div>
        </div>
        <div className="text-center py-8">
          <p className="text-muted-foreground">
            {grade === 'A+' 
              ? `Excellent work! Your documentation meets all requirements with strong evidence. Current grade: ${grade}`
              : 'No specific recommendations available. Please ensure audit data is complete.'
            }
          </p>
        </div>
      </div>
    );
  }
  
  const getPriorityColor = (priority: string) => {
    switch (priority?.toLowerCase()) {
      case 'critical':
        return 'border-red-500 bg-red-500/10 text-red-600';
      case 'high':
        return 'border-orange-500 bg-orange-500/10 text-orange-600';
      case 'medium':
        return 'border-yellow-500 bg-yellow-500/10 text-yellow-600';
      default:
        return 'border-blue-500 bg-blue-500/10 text-blue-600';
    }
  };

  return (
    <div className="bg-card rounded-lg border border-border p-6">
      {/* Header with View Detailed Analysis Button */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <TrendingUp className="text-primary" size={24} />
          </div>
          <div>
            <h3 className="text-xl font-bold">{roadmapTitle}</h3>
            <p className="text-sm text-muted-foreground">
              {roadmapDescription}
            </p>
          </div>
        </div>
        <button
          onClick={viewDetailedRecommendations}
          className="px-6 py-3 bg-gradient-to-r from-primary to-accent text-white rounded-lg hover:opacity-90 transition-all flex items-center gap-2 shadow-lg hover:shadow-xl animate-pulse"
        >
          <BarChart3 size={20} />
          <span className="font-bold">View Detailed Analysis</span>
          <Sparkles size={20} />
        </button>
      </div>
      
      <div className="space-y-6">
        {actionableRecommendations.map((rec, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.15 }}
            className="rounded-xl border border-border bg-background/50 p-6 hover:shadow-lg transition-all"
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start gap-3 flex-1">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-sm font-bold text-primary">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-lg mb-1">{rec.title}</h4>
                  <p className="text-sm text-muted-foreground">{rec.description}</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(rec.priority)}`}>
                {rec.priority}
              </span>
            </div>
            
            {/* Action Items */}
            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-2">
                <Target size={16} />
                <span>Action Items:</span>
              </div>
              {rec.actions.map((action, actionIndex) => (
                <div key={actionIndex} className="flex items-start gap-3 pl-6">
                  <CheckCircle2 size={16} className="text-green-500 flex-shrink-0 mt-0.5" />
                  <p className="text-sm flex-1">{action}</p>
                </div>
              ))}
            </div>
            
            {/* Impact */}
            <div className="flex items-center gap-2 pt-4 border-t border-border/50">
              <Lightbulb size={16} className="text-yellow-500" />
              <span className="text-sm font-medium">Expected Impact:</span>
              <span className="text-sm text-primary">{rec.impact}</span>
            </div>
          </motion.div>
        ))}
        
        {/* Summary Card with Detailed Analysis Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: actionableRecommendations.length * 0.15 }}
          className="rounded-xl border-2 border-primary/30 bg-primary/5 p-6"
        >
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-lg bg-primary/20">
              <ArrowRight className="text-primary" size={24} />
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-lg mb-2">Next Steps: {grade} → {targetGrade}</h4>
              <p className="text-sm text-muted-foreground mb-4">
                {grade === 'A+' 
                  ? `You've achieved ${grade} grade. Continue maintaining excellence through systematic documentation and continuous improvement. Regular internal audits will help sustain this high standard.`
                  : `Start with Critical and High priority items first. Focus on collecting comprehensive evidence with specific numbers, dates, and supporting documents. Systematic improvement will help you achieve ${targetGrade} grade in the next assessment cycle.`
                }
              </p>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm font-medium text-primary">
                  <span>
                    {grade === 'A+' 
                      ? 'Timeline: Continuous maintenance and enhancement'
                      : confidence < 0.5 
                      ? 'Timeline: 9-12 months for significant improvement'
                      : 'Timeline: 6-9 months for grade improvement'
                    }
                  </span>
                </div>
                <button
                  onClick={viewDetailedRecommendations}
                  className="ml-auto px-6 py-3 bg-gradient-to-r from-primary to-accent text-white rounded-lg hover:opacity-90 transition-all flex items-center gap-2 shadow-lg hover:shadow-xl font-bold"
                >
                  <BarChart3 size={20} />
                  View Full Analysis with Charts
                  <ArrowRight size={20} />
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
