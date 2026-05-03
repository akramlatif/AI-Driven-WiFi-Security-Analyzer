import React, { useState } from 'react';
import NetworkList from '../components/NetworkList';

export default function NetworkScanner({ onScanComplete }) {
  const [loading, setLoading] = useState(false);
  const [networks, setNetworks] = useState([]);
  const [error, setError] = useState(null);
  const [simulate, setSimulate] = useState(true);
  const [scanProgress, setScanProgress] = useState(0);

  const handleScan = async () => {
    setLoading(true);
    setError(null);
    setScanProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setScanProgress(prev => Math.min(prev + Math.random() * 40, 90));
      }, 300);

      const response = await fetch('http://localhost:5000/api/scan-networks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ simulate }),
      });

      clearInterval(progressInterval);
      setScanProgress(100);

      if (!response.ok) throw new Error('Scan failed');

      const data = await response.json();
      if (data.success) {
        setNetworks(data.networks);
        onScanComplete(data);
      } else {
        setError(data.error || 'Scan failed');
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
      setTimeout(() => setScanProgress(0), 500);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-900/20 to-cyan-900/20 border border-blue-500/30 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Network Scanner</h2>
        <p className="text-blue-400">Scan nearby WiFi networks and assess security risks</p>
      </div>

      {/* Controls */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
        <div className="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4">
          <label className="flex items-center space-x-3 cursor-pointer flex-1">
            <input
              type="checkbox"
              checked={simulate}
              onChange={(e) => setSimulate(e.target.checked)}
              disabled={loading}
              className="w-4 h-4 rounded accent-cyan-500"
            />
            <span className="text-white font-medium">Use sample data (recommended for demo)</span>
          </label>
          <button
            onClick={handleScan}
            disabled={loading}
            className="bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-lg transition-all duration-200 flex items-center space-x-2 whitespace-nowrap"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Scanning...</span>
              </>
            ) : (
              <>
                <span>🔍</span>
                <span>Start Scan</span>
              </>
            )}
          </button>
        </div>

        {/* Progress Bar */}
        {loading && (
          <div className="mt-4">
            <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
              <div
                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full transition-all duration-300"
                style={{ width: `${scanProgress}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-400 mt-2">{Math.floor(scanProgress)}% complete</p>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-600/20 border border-red-500/50 rounded-lg p-4 text-red-400">
          <p className="font-semibold">❌ Error: {error}</p>
        </div>
      )}

      {/* Results Summary */}
      {networks.length > 0 && !loading && (
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-red-600/20 border border-red-500/50 rounded-lg p-4 text-center">
            <p className="text-red-400 text-sm font-semibold uppercase">High Risk</p>
            <p className="text-3xl font-bold text-white mt-2">{networks.filter(n => n.risk_label === 'High').length}</p>
          </div>
          <div className="bg-yellow-600/20 border border-yellow-500/50 rounded-lg p-4 text-center">
            <p className="text-yellow-400 text-sm font-semibold uppercase">Medium Risk</p>
            <p className="text-3xl font-bold text-white mt-2">{networks.filter(n => n.risk_label === 'Medium').length}</p>
          </div>
          <div className="bg-green-600/20 border border-green-500/50 rounded-lg p-4 text-center">
            <p className="text-green-400 text-sm font-semibold uppercase">Low Risk</p>
            <p className="text-3xl font-bold text-white mt-2">{networks.filter(n => n.risk_label === 'Low').length}</p>
          </div>
        </div>
      )}

      {/* Network List */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Detected Networks ({networks.length})</h3>
        <NetworkList networks={networks} loading={loading} />
      </div>
    </div>
  );
}
