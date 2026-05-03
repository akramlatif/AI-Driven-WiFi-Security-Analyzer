import React, { useState } from 'react';

export default function Reports() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateReport = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/generate-report');
      if (!response.ok) throw new Error('Failed to generate report');

      const data = await response.json();
      if (data.success) {
        setReport(data.report);
      } else {
        setError(data.error || 'Failed to generate report');
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = () => {
    if (!report) return;
    
    const element = document.createElement('a');
    const file = new Blob([report], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `wifi_security_report_${new Date().toISOString().slice(0, 19).replace(/:/g, '')}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-900/20 to-emerald-900/20 border border-green-500/30 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Security Reports</h2>
        <p className="text-green-400">Generate and download comprehensive security assessments</p>
      </div>

      {/* Generate Button */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">Generate Report</h3>
            <p className="text-gray-400 text-sm">Create a detailed security assessment report</p>
          </div>
          <button
            onClick={handleGenerateReport}
            disabled={loading}
            className="mt-4 md:mt-0 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-lg transition-all duration-200 flex items-center space-x-2 whitespace-nowrap"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                </svg>
                <span>Generating...</span>
              </>
            ) : (
              <>
                <span>📄</span>
                <span>Generate Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-600/20 border border-red-500/50 rounded-lg p-4 text-red-400">
          <p className="font-semibold">❌ Error: {error}</p>
        </div>
      )}

      {/* Report Display */}
      {report && (
        <div className="space-y-4">
          {/* Download Button */}
          <button
            onClick={handleDownloadReport}
            className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200 flex items-center space-x-2"
          >
            <span>⬇️</span>
            <span>Download Report</span>
          </button>

          {/* Report Content */}
          <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
            <div className="prose prose-invert max-w-none">
              <div className="bg-slate-900 rounded p-6 text-gray-300 font-mono text-sm max-h-96 overflow-y-auto whitespace-pre-wrap break-words">
                {report}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Placeholder */}
      {!report && !loading && (
        <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-12 text-center">
          <p className="text-gray-400 mb-4">📊 No report generated yet</p>
          <p className="text-gray-500 text-sm">Click the button above to generate a security report</p>
        </div>
      )}
    </div>
  );
}
