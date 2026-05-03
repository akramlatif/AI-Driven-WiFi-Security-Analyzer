import React from 'react';

export default function MetricCard({ title, value, icon, color, trend, description }) {
  const colorClasses = {
    red: 'from-red-600 to-red-900',
    yellow: 'from-amber-600 to-amber-900',
    green: 'from-green-600 to-green-900',
    blue: 'from-blue-600 to-blue-900',
    cyan: 'from-cyan-600 to-cyan-900',
  };

  return (
    <div className={`bg-gradient-to-br ${colorClasses[color] || colorClasses.blue} rounded-lg p-6 border border-opacity-20 border-white hover:shadow-lg hover:shadow-${color}-500/20 transition-all duration-300 transform hover:scale-105`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-300 font-medium uppercase tracking-wider">{title}</p>
          <p className="text-4xl font-bold mt-2 text-white">{value}</p>
          {description && (
            <p className="text-xs text-gray-400 mt-2">{description}</p>
          )}
          {trend && (
            <div className={`flex items-center mt-2 text-sm ${trend > 0 ? 'text-red-400' : 'text-green-400'}`}>
              <svg className={`w-4 h-4 mr-1 transform ${trend > 0 ? 'rotate-0' : 'rotate-180'}`} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414-1.414L13.586 7H12z" clipRule="evenodd" />
              </svg>
              {Math.abs(trend)}% {trend > 0 ? 'increase' : 'decrease'}
            </div>
          )}
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );
}
