import React from 'react';

export default function AlertCard({ alert, index }) {
  const severityColors = {
    critical: 'from-red-600 to-red-900 border-red-500',
    high: 'from-orange-600 to-orange-900 border-orange-500',
    medium: 'from-yellow-600 to-yellow-900 border-yellow-500',
    low: 'from-blue-600 to-blue-900 border-blue-500',
    info: 'from-cyan-600 to-cyan-900 border-cyan-500',
  };

  const severityIcons = {
    critical: '🚨',
    high: '⚠️',
    medium: '⚡',
    low: 'ℹ️',
    info: 'ℹ️',
  };

  const severity = alert.severity || 'info';

  return (
    <div className={`bg-gradient-to-r ${severityColors[severity]} border rounded-lg p-4 animate-fade-in`} style={{ animationDelay: `${index * 100}ms` }}>
      <div className="flex items-start space-x-3">
        <span className="text-2xl mt-1">{severityIcons[severity]}</span>
        <div className="flex-1">
          <p className="font-semibold text-white text-sm uppercase tracking-wide">{alert.type}</p>
          <p className="text-gray-200 mt-1">{alert.message}</p>
          <p className="text-xs text-gray-400 mt-2">{new Date(alert.timestamp).toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}
