'use client';

import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface DimensionCoverageChartProps {
  dimensions: Array<{
    name: string;
    coverage: number;
    found: boolean;
  }>;
}

export default function DimensionCoverageChart({ dimensions }: DimensionCoverageChartProps) {
  const data = {
    labels: dimensions.map(d => d.name.length > 20 ? d.name.substring(0, 20) + '...' : d.name),
    datasets: [
      {
        label: 'Coverage %',
        data: dimensions.map(d => d.coverage * 100),
        backgroundColor: dimensions.map(d => 
          d.found ? 'rgba(16, 185, 129, 0.8)' : 'rgba(239, 68, 68, 0.8)'
        ),
        borderColor: dimensions.map(d => 
          d.found ? 'rgb(16, 185, 129)' : 'rgb(239, 68, 68)'
        ),
        borderWidth: 2,
        borderRadius: 8,
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
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleColor: '#fff',
        bodyColor: '#fff',
        callbacks: {
          label: function(context: any) {
            return `Coverage: ${context.parsed.y.toFixed(1)}%`;
          }
        }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: any) {
            return value + '%';
          },
          color: '#9ca3af',
        },
        grid: {
          color: 'rgba(156, 163, 175, 0.1)',
        },
      },
      x: {
        ticks: {
          color: '#9ca3af',
          maxRotation: 45,
          minRotation: 45,
        },
        grid: {
          display: false,
        },
      },
    },
    animation: {
      duration: 1500,
      easing: 'easeInOutQuart' as const,
    },
  };

  return (
    <div className="w-full h-80">
      <Bar data={data} options={options} />
    </div>
  );
}
