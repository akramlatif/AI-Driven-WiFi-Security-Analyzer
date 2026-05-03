import React from 'react';

export default function NetworkList({ networks, loading }) {
  const getRiskColor = (risk) => {
    switch(risk) {
      case 'High': return 'border-red-500 bg-red-500/10 text-red-400';
      case 'Medium': return 'border-yellow-500 bg-yellow-500/10 text-yellow-400';
      case 'Low': return 'border-green-500 bg-green-500/10 text-green-400';
      default: return 'border-gray-500 bg-gray-500/10 text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="h-20 bg-slate-800 rounded-lg animate-pulse"></div>
        ))}
      </div>
    );
  }

  if (!networks || networks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">No networks scanned yet. Start a scan to see results.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3 max-h-96 overflow-y-auto">
      {networks.map(network => (
        <div
          key={network.id}
          className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 hover:border-slate-600 transition-all hover:shadow-lg hover:shadow-slate-900/50"
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3">
                <span className="text-xl">📶</span>
                <div>
                  <p className="font-semibold text-white">{network.ssid}</p>
                  <div className="flex items-center space-x-4 mt-1 text-xs text-gray-400">
                    <span>🔒 {network.encryption}</span>
                    <span>📊 Ch: {network.channel}</span>
                    <span>📡 Signal: {network.signal}%</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className="text-right">
                <div className={`font-bold border rounded-full px-3 py-1 text-xs ${getRiskColor(network.risk_label)}`}>
                  {network.risk_label}
                </div>
                <p className="text-sm text-gray-400 mt-1">Score: {network.risk_score}</p>
              </div>
              {network.threat_count > 0 && (
                <div className="bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                  {network.threat_count}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
