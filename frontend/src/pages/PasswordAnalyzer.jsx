import React, { useState } from 'react';

export default function PasswordAnalyzer() {
  const [password, setPassword] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  const handleAnalyze = async () => {
    if (!password) {
      setError('Please enter a password');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/analyze-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      if (!response.ok) throw new Error('Analysis failed');

      const data = await response.json();
      if (data.success) {
        setResult(data.password_analysis);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const getStrengthColor = (strength) => {
    if (!strength) return 'bg-gray-500';
    const lower = strength.toLowerCase();
    if (lower.includes('very weak')) return 'bg-red-600';
    if (lower.includes('weak')) return 'bg-orange-600';
    if (lower.includes('fair')) return 'bg-yellow-600';
    if (lower.includes('good')) return 'bg-blue-600';
    if (lower.includes('strong')) return 'bg-green-600';
    return 'bg-cyan-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-900/20 to-red-900/20 border border-orange-500/30 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Password Strength Analyzer</h2>
        <p className="text-orange-400">Evaluate password security and weakness patterns</p>
      </div>

      {/* Input Section */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-8 max-w-2xl">
        <label className="block text-white font-semibold mb-4">Test Password</label>
        <div className="relative mb-4">
          <input
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
            placeholder="Enter password to analyze..."
            disabled={loading}
            className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 disabled:opacity-50"
          />
          <button
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-3.5 text-gray-400 hover:text-cyan-400"
          >
            {showPassword ? '👁️' : '👁️‍🗨️'}
          </button>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading || !password}
          className="w-full bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-6 rounded-lg transition-all duration-200"
        >
          {loading ? '🔄 Analyzing...' : '🔐 Analyze Password'}
        </button>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-600/20 border border-red-500/50 rounded-lg p-4 text-red-400">
          <p className="font-semibold">❌ Error: {error}</p>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="space-y-4">
          {/* Strength Indicator */}
          <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Password Strength</h3>
            <div className={`${getStrengthColor(result.strength)} rounded-lg p-6 text-white text-center`}>
              <p className="text-4xl font-bold mb-2">{result.strength || 'Unknown'}</p>
              <p className="text-sm opacity-90">Estimated crack time: {result.crack_time || 'Unknown'}</p>
            </div>
          </div>

          {/* Recommendations */}
          {result.recommendations && result.recommendations.length > 0 && (
            <div className="bg-blue-600/20 border border-blue-500/50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-400 mb-4">💡 Recommendations</h3>
              <ul className="space-y-2">
                {result.recommendations.map((rec, i) => (
                  <li key={i} className="text-blue-300 flex items-start space-x-3">
                    <span className="text-lg">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Analysis Details */}
          {result.analysis && (
            <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">📊 Analysis Details</h3>
              <div className="space-y-3 text-sm">
                {Object.entries(result.analysis).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center py-2 border-b border-slate-700">
                    <span className="text-gray-400 capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="text-white font-semibold">{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Initial State */}
      {!result && !loading && password && (
        <div className="text-center py-12 bg-slate-800/20 border border-slate-700 rounded-lg">
          <p className="text-gray-400">Enter a password and click analyze to get started</p>
        </div>
      )}
    </div>
  );
}
