import React, { useState } from 'react';

export default function TrafficAnalysis() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/analyze-traffic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.traffic_analysis);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-900/20 to-pink-900/20 border border-purple-500/30 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Traffic Anomaly Analysis</h2>
        <p className="text-purple-400">Detect unusual network traffic patterns and behaviors</p>
      </div>

      {/* Control */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-lg transition-all duration-200 flex items-center space-x-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              </svg>
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <span>📡</span>
              <span>Analyze Traffic</span>
            </>
          )}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Analysis Results</h3>
          <div className="bg-slate-700/30 rounded p-4 text-gray-300 font-mono text-sm max-h-96 overflow-y-auto">
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        </div>
      )}

      {/* Placeholder */}
      {!result && !loading && (
        <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-12 text-center">
          <p className="text-gray-400 mb-4">Click the analyze button to start traffic analysis</p>
          <p className="text-gray-500 text-sm">Real-time packet inspection and anomaly detection</p>
        </div>
      )}
    </div>
  );
}
