'use client';

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

interface FundingAgencyChartProps {
  agencies: Array<{
    name: string;
    amount: number;
    projects: number;
  }>;
}

export default function FundingAgencyChart({ agencies }: FundingAgencyChartProps) {
  const colors = [
    'rgba(6, 182, 212, 0.8)',   // Cyan
    'rgba(168, 85, 247, 0.8)',  // Purple
    'rgba(236, 72, 153, 0.8)',  // Pink
    'rgba(251, 146, 60, 0.8)',  // Orange
    'rgba(34, 197, 94, 0.8)',   // Green
    'rgba(59, 130, 246, 0.8)',  // Blue
  ];

  const data = {
    labels: agencies.map(a => a.name),
    datasets: [
      {
        data: agencies.map(a => a.amount),
        backgroundColor: colors.slice(0, agencies.length),
        borderColor: colors.slice(0, agencies.length).map(c => c.replace('0.8', '1')),
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right' as const,
        labels: {
          color: '#9ca3af',
          padding: 15,
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        callbacks: {
          label: function(context: any) {
            const agency = agencies[context.dataIndex];
            return [
              `Amount: ₹${agency.amount} Lakhs`,
              `Projects: ${agency.projects}`,
            ];
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
    <div className="w-full h-80">
      <Pie data={data} options={options} />
    </div>
  );
}
