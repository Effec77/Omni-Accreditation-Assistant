"use client";

import { useState } from "react";
import { CheckCircle, Table as TableIcon, BarChart3, FileText, TrendingUp, Building2, Calendar } from "lucide-react";

interface EvidenceItem {
  child_text: string;
  reranker_score: number;
  source: string;
  metadata?: Record<string, any>;
}

interface EvidenceTableVisualizerProps {
  evidence: EvidenceItem[];
  dimensions: string[];
}

// Extract structured data from evidence text - IMPROVED VERSION
function extractTableData(text: string): { type: string; data: any[]; summary: any } | null {
  const summary = {
    totalProjects: 0,
    totalFunding: 0,
    agencies: new Set<string>(),
    years: new Set<string>()
  };
  
  // Split by common delimiters and clean
  const cleanText = text.replace(/\s+/g, ' ').trim();
  
  // Pattern 1: Look for explicit table markers
  if (cleanText.includes('Table') && (cleanText.includes('Year') || cleanText.includes('Projects') || cleanText.includes('Funding'))) {
    const rows: any[] = [];
    
    // Extract year patterns: 2019-20, 2020-21, etc.
    const yearMatches = cleanText.match(/(\d{4}-\d{2})/g) || [];
    
    // Extract project numbers: "Projects: 22" or "22 projects" or just numbers near "Projects"
    const projectMatches = cleanText.match(/(?:Projects?:?\s*|Number of Projects:?\s*)(\d+)|(\d+)\s+projects?/gi) || [];
    const projectNumbers = projectMatches.map(m => {
      const num = m.match(/\d+/);
      return num ? parseInt(num[0]) : 0;
    });
    
    // Extract funding: "785 Lakhs" or "Funding: 785" or "₹785"
    const fundingMatches = cleanText.match(/(?:Funding|Total|Amount)[:\s]*(?:₹|INR|Rs\.?)?\s*(\d+(?:,\d+)?)\s*(?:Lakhs?|Crore)?/gi) || [];
    const fundingNumbers = fundingMatches.map(m => {
      const num = m.match(/(\d+(?:,\d+)?)/);
      return num ? parseInt(num[1].replace(/,/g, '')) : 0;
    });
    
    // Extract agencies
    const agencyPattern = /(DST|SERB|DBT|ICSSR|Industry|Corporate|UGC|AICTE|Government)/gi;
    const agencyMatches = cleanText.match(agencyPattern) || [];
    const uniqueAgencies = Array.from(new Set(agencyMatches.map(a => a.toUpperCase())));
    
    // Build rows by matching indices
    const maxRows = Math.max(yearMatches.length, projectNumbers.length, fundingNumbers.length);
    
    for (let i = 0; i < maxRows; i++) {
      const year = yearMatches[i] || '';
      const projects = projectNumbers[i] || 0;
      const funding = fundingNumbers[i] || 0;
      const agencies = uniqueAgencies.slice(i * 2, (i + 1) * 2).join(', ') || uniqueAgencies.join(', ');
      
      if (year || projects || funding) {
        rows.push({ year, projects, funding, agencies });
        summary.totalProjects += projects;
        summary.totalFunding += funding;
        if (year) summary.years.add(year);
      }
    }
    
    uniqueAgencies.forEach(a => summary.agencies.add(a));
    
    if (rows.length > 0) {
      return { type: 'year-wise', data: rows, summary };
    }
  }
  
  // Pattern 2: Agency-focused data
  const agencyPattern = /(DST|SERB|DBT|ICSSR|Industry|Corporate)/gi;
  const agencies = cleanText.match(agencyPattern);
  
  if (agencies && agencies.length > 0) {
    const agencyData: any[] = [];
    const uniqueAgencies = Array.from(new Set(agencies.map(a => a.toUpperCase())));
    
    // Try to find numbers associated with each agency
    uniqueAgencies.forEach(agency => {
      const agencyIndex = cleanText.toUpperCase().indexOf(agency);
      const contextAfter = cleanText.substring(agencyIndex, agencyIndex + 200);
      
      const projectMatch = contextAfter.match(/(\d+)\s*(?:projects?|Projects?)/i);
      const fundingMatch = contextAfter.match(/(?:₹|INR|Rs\.?)?\s*(\d+(?:,\d+)?)\s*(?:Lakhs?|Crore)/i);
      
      const projects = projectMatch ? parseInt(projectMatch[1]) : 0;
      const funding = fundingMatch ? parseInt(fundingMatch[1].replace(/,/g, '')) : 0;
      
      if (projects || funding) {
        agencyData.push({ agency, projects, funding });
        summary.totalProjects += projects;
        summary.totalFunding += funding;
        summary.agencies.add(agency);
      }
    });
    
    if (agencyData.length > 0) {
      return { type: 'agency-wise', data: agencyData, summary };
    }
  }
  
  return null;
}

export default function EvidenceTableVisualizer({ evidence, dimensions }: EvidenceTableVisualizerProps) {
  const [viewMode, setViewMode] = useState<'table' | 'chart'>('table');
  
  // Extract structured data from all evidence
  const structuredEvidence = evidence
    .map(e => ({
      ...e,
      structured: extractTableData(e.child_text)
    }))
    .filter(e => e.structured !== null);
  
  // Aggregate summary across all evidence
  const globalSummary = {
    totalProjects: 0,
    totalFunding: 0,
    agencies: new Set<string>(),
    years: new Set<string>()
  };
  
  structuredEvidence.forEach(e => {
    if (e.structured) {
      globalSummary.totalProjects += e.structured.summary.totalProjects;
      globalSummary.totalFunding += e.structured.summary.totalFunding;
      e.structured.summary.agencies.forEach((a: string) => globalSummary.agencies.add(a));
      e.structured.summary.years.forEach((y: string) => globalSummary.years.add(y));
    }
  });

  // If no structured data found, show message
  if (structuredEvidence.length === 0) {
    return (
      <div className="glass-card p-8 rounded-xl text-center">
        <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
        <p className="text-muted-foreground mb-2">No structured data found in evidence</p>
        <p className="text-sm text-muted-foreground">
          Switch to "List" view to see raw evidence text
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-4 rounded-xl border border-accent/20">
          <div className="flex items-center gap-2 text-muted-foreground mb-2">
            <BarChart3 size={18} className="text-accent" />
            <span className="text-sm font-medium">Total Projects</span>
          </div>
          <p className="text-3xl font-bold text-accent">{globalSummary.totalProjects}</p>
          <p className="text-xs text-muted-foreground mt-1">Funded projects</p>
        </div>
        
        <div className="glass-card p-4 rounded-xl border border-accent/20">
          <div className="flex items-center gap-2 text-muted-foreground mb-2">
            <TrendingUp size={18} className="text-accent" />
            <span className="text-sm font-medium">Total Funding</span>
          </div>
          <p className="text-3xl font-bold text-accent">₹{globalSummary.totalFunding.toLocaleString()}</p>
          <p className="text-xs text-muted-foreground mt-1">Lakhs</p>
        </div>
        
        <div className="glass-card p-4 rounded-xl border border-accent/20">
          <div className="flex items-center gap-2 text-muted-foreground mb-2">
            <Building2 size={18} className="text-accent" />
            <span className="text-sm font-medium">Funding Agencies</span>
          </div>
          <p className="text-3xl font-bold text-accent">{globalSummary.agencies.size}</p>
          <p className="text-xs text-muted-foreground mt-1">Unique sources</p>
        </div>
        
        <div className="glass-card p-4 rounded-xl border border-accent/20">
          <div className="flex items-center gap-2 text-muted-foreground mb-2">
            <Calendar size={18} className="text-accent" />
            <span className="text-sm font-medium">Time Period</span>
          </div>
          <p className="text-3xl font-bold text-accent">{globalSummary.years.size}</p>
          <p className="text-xs text-muted-foreground mt-1">Years covered</p>
        </div>
      </div>

      {/* View Toggle */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => setViewMode('table')}
          className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
            viewMode === 'table'
              ? 'bg-accent text-accent-foreground shadow-lg'
              : 'glass-card text-muted-foreground hover:text-foreground hover:border-accent/30'
          }`}
        >
          <TableIcon size={16} />
          Table View
        </button>
        <button
          onClick={() => setViewMode('chart')}
          className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
            viewMode === 'chart'
              ? 'bg-accent text-accent-foreground shadow-lg'
              : 'glass-card text-muted-foreground hover:text-foreground hover:border-accent/30'
          }`}
        >
          <BarChart3 size={16} />
          Chart View
        </button>
      </div>

      {/* Data Display */}
      {viewMode === 'table' ? (
        <div className="space-y-4">
          {structuredEvidence.map((e, idx) => (
            <div key={idx} className="glass-card rounded-xl overflow-hidden border border-border/50">
              <div className="bg-gradient-to-r from-accent/20 to-accent/10 px-6 py-4 border-b border-border/50">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-foreground flex items-center gap-2">
                    <CheckCircle size={18} className="text-accent" />
                    {e.structured?.type === 'year-wise' ? 'Year-wise Funding Data' : 'Agency-wise Funding Data'}
                  </h3>
                  <div className="flex items-center gap-2">
                    <div className="px-3 py-1 bg-accent/20 rounded-full">
                      <span className="text-sm font-medium text-accent">
                        {Math.round(e.reranker_score * 100)}% relevant
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-muted/50 border-b border-border/50">
                    <tr>
                      {e.structured?.type === 'year-wise' ? (
                        <>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Year</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Projects</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Funding (₹ Lakhs)</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Agencies</th>
                        </>
                      ) : (
                        <>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Agency</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Projects</th>
                          <th className="px-6 py-4 text-left text-sm font-semibold text-foreground">Funding (₹ Lakhs)</th>
                        </>
                      )}
                    </tr>
                  </thead>
                  <tbody>
                    {e.structured?.data.map((row: any, rowIdx: number) => (
                      <tr key={rowIdx} className="border-b border-border/30 hover:bg-accent/5 transition-colors">
                        {e.structured?.type === 'year-wise' ? (
                          <>
                            <td className="px-6 py-4 text-sm text-foreground font-medium">{row.year || '-'}</td>
                            <td className="px-6 py-4 text-sm text-foreground">{row.projects || '-'}</td>
                            <td className="px-6 py-4 text-sm text-accent font-semibold">{row.funding ? `₹${row.funding.toLocaleString()}` : '-'}</td>
                            <td className="px-6 py-4 text-sm text-muted-foreground">{row.agencies || '-'}</td>
                          </>
                        ) : (
                          <>
                            <td className="px-6 py-4 text-sm text-foreground font-semibold">{row.agency || '-'}</td>
                            <td className="px-6 py-4 text-sm text-foreground">{row.projects || '-'}</td>
                            <td className="px-6 py-4 text-sm text-accent font-semibold">{row.funding ? `₹${row.funding.toLocaleString()}` : '-'}</td>
                          </>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="px-6 py-3 bg-muted/20 border-t border-border/30 flex items-center gap-2">
                <FileText size={14} className="text-muted-foreground" />
                <span className="text-xs text-muted-foreground">Source: {e.source}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="glass-card p-8 rounded-xl border border-border/50">
          <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
            <BarChart3 className="text-accent" />
            Funding Distribution by Agency
          </h3>
          <div className="space-y-6">
            {Array.from(globalSummary.agencies).map((agency, idx) => {
              const agencyData = structuredEvidence
                .flatMap(e => e.structured?.data || [])
                .filter((row: any) => row.agency?.toUpperCase() === agency);
              
              const totalFunding = agencyData.reduce((sum: number, row: any) => 
                sum + (row.funding || 0), 0
              );
              
              const totalProjects = agencyData.reduce((sum: number, row: any) => 
                sum + (row.projects || 0), 0
              );
              
              const maxFunding = Math.max(...Array.from(globalSummary.agencies).map(a => {
                const data = structuredEvidence
                  .flatMap(e => e.structured?.data || [])
                  .filter((row: any) => row.agency?.toUpperCase() === a);
                return data.reduce((sum: number, row: any) => sum + (row.funding || 0), 0);
              }));
              
              const percentage = maxFunding > 0 ? (totalFunding / maxFunding) * 100 : 0;
              
              return (
                <div key={idx} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-foreground font-semibold text-lg">{agency}</span>
                      <p className="text-sm text-muted-foreground">{totalProjects} projects</p>
                    </div>
                    <span className="text-accent font-bold text-xl">₹{totalFunding.toLocaleString()} L</span>
                  </div>
                  <div className="h-10 bg-muted/30 rounded-lg overflow-hidden border border-border/30">
                    <div
                      className="h-full bg-gradient-to-r from-accent/90 to-accent flex items-center px-4 transition-all duration-700 ease-out"
                      style={{ width: `${percentage}%` }}
                    >
                      {percentage > 15 && (
                        <span className="text-sm font-medium text-accent-foreground">
                          {percentage.toFixed(0)}%
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
