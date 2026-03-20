'use client';

import { useEffect, useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

interface InteractiveConfidenceChartProps {
  confidenceScore: number;
  grade: string;
}

export default function InteractiveConfidenceChart({ 
  confidenceScore, 
  grade 
}: InteractiveConfidenceChartProps) {
  const percentage = Math.round(confidenceScore * 100);
  
  // Color based on score
  const getColor = () => {
    if (percentage >= 75) return { main: '#10b981', bg: '#10b98120' }; // Green
    if (percentage >= 50) return { main: '#f59e0b', bg: '#f59e0b20' }; // Orange
    if (percentage >= 25) return { main: '#ef4444', bg: '#ef444420' }; // Red
    return { main: '#6b7280', bg: '#6b728020' }; // Gray
  };

  const colors = getColor();

  const data = {
    labels: ['Confidence', 'Gap'],
    datasets: [
      {
        data: [percentage, 100 - percentage],
        backgroundColor: [colors.main, colors.bg],
        borderColor: [colors.main, 'transparent'],
        borderWidth: 2,
        cutout: '75%',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: true,
        callbacks: {
          label: function(context: any) {
            return context.label + ': ' + context.parsed + '%';
          }
        }
      },
    },
    animation: {
      animateRotate: true,
      animateScale: true,
      duration: 1500,
      easing: 'easeInOutQuart' as const,
    },
  };

  return (
    <div className="relative w-full h-64">
      <Doughnut data={data} options={options} />
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <div className="text-5xl font-bold" style={{ color: colors.main }}>
          {percentage}%
        </div>
        <div className="text-sm text-muted-foreground mt-2">
          Grade {grade}
        </div>
      </div>
    </div>
  );
}
