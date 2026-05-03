import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function RiskChart({ data }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !data) return;

    // Destroy previous chart
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const ctx = canvasRef.current.getContext('2d');
    
    chartRef.current = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: data.map(d => d.label),
        datasets: [
          {
            data: data.map(d => d.count),
            backgroundColor: data.map(d => d.color),
            borderColor: '#0f172a',
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#d1d5db',
              font: { size: 12, weight: 'bold' },
              usePointStyle: true,
              padding: 20,
            },
          },
        },
      },
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [data]);

  return (
    <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Risk Distribution</h3>
      <canvas ref={canvasRef}></canvas>
    </div>
  );
}
