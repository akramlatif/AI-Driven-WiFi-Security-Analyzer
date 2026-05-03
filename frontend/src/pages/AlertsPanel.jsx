import React, { useState, useEffect } from 'react';
import AlertCard from '../components/AlertCard';

export default function AlertsPanel() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedSeverity, setSelectedSeverity] = useState('all');

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/generate-alerts');
        if (response.ok) {
          const data = await response.json();
          setAlerts(data.alerts || []);
        }
      } catch (error) {
        console.error('Error fetching alerts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const filteredAlerts = selectedSeverity === 'all'
    ? alerts
    : alerts.filter(a => a.severity === selectedSeverity);

  const severityCount = {
    critical: alerts.filter(a => a.severity === 'critical').length,
    high: alerts.filter(a => a.severity === 'high').length,
    medium: alerts.filter(a => a.severity === 'medium').length,
    low: alerts.filter(a => a.severity === 'low').length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-900/20 to-orange-900/20 border border-red-500/30 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-white mb-2">Security Alerts</h2>
        <p className="text-red-400">Monitor and manage security events in real-time</p>
      </div>

      {/* Alert Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className={`rounded-lg p-4 cursor-pointer transition-all ${selectedSeverity === 'all' ? 'bg-blue-600/30 border border-blue-500' : 'bg-slate-800/30 border border-slate-700'}`} onClick={() => setSelectedSeverity('all')}>
          <p className="text-gray-400 text-sm">Total Alerts</p>
          <p className="text-3xl font-bold text-white">{alerts.length}</p>
        </div>
        <div className={`rounded-lg p-4 cursor-pointer transition-all ${selectedSeverity === 'critical' ? 'bg-red-600/30 border border-red-500' : 'bg-slate-800/30 border border-slate-700'}`} onClick={() => setSelectedSeverity('critical')}>
          <p className="text-red-400 text-sm">🚨 Critical</p>
          <p className="text-3xl font-bold text-red-400">{severityCount.critical}</p>
        </div>
        <div className={`rounded-lg p-4 cursor-pointer transition-all ${selectedSeverity === 'high' ? 'bg-orange-600/30 border border-orange-500' : 'bg-slate-800/30 border border-slate-700'}`} onClick={() => setSelectedSeverity('high')}>
          <p className="text-orange-400 text-sm">⚠️ High</p>
          <p className="text-3xl font-bold text-orange-400">{severityCount.high}</p>
        </div>
        <div className={`rounded-lg p-4 cursor-pointer transition-all ${selectedSeverity === 'medium' ? 'bg-yellow-600/30 border border-yellow-500' : 'bg-slate-800/30 border border-slate-700'}`} onClick={() => setSelectedSeverity('medium')}>
          <p className="text-yellow-400 text-sm">⚡ Medium</p>
          <p className="text-3xl font-bold text-yellow-400">{severityCount.medium}</p>
        </div>
      </div>

      {/* Alerts List */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
          <span>📋</span>
          <span>Alert Timeline</span>
        </h3>
        
        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-24 bg-slate-700 rounded-lg animate-pulse"></div>
            ))}
          </div>
        ) : filteredAlerts.length > 0 ? (
          <div className="space-y-3 max-h-96 overflow-y-auto pr-4">
            {filteredAlerts.map((alert, idx) => (
              <AlertCard key={idx} alert={alert} index={idx} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-400">✨ No alerts in this category</p>
          </div>
        )}
      </div>
    </div>
  );
}
