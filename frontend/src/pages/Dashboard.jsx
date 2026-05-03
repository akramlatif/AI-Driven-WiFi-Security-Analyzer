import React, { useState, useEffect } from 'react';
import MetricCard from '../components/MetricCard';
import AlertCard from '../components/AlertCard';
import NetworkList from '../components/NetworkList';
import RiskChart from '../components/RiskChart';

export default function Dashboard({ scanData }) {
  const [metrics, setMetrics] = useState({
    total: 0,
    high_risk: 0,
    medium_risk: 0,
    low_risk: 0,
  });
  const [risk_distribution, setRiskDistribution] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [networks, setNetworks] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load initial data
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch risk distribution
        const riskRes = await fetch('http://localhost:5000/api/risk-distribution');
        if (riskRes.ok) {
          const riskData = await riskRes.json();
          setRiskDistribution(riskData.distribution || []);
        }

        // Fetch alerts
        const alertsRes = await fetch('http://localhost:5000/api/generate-alerts');
        if (alertsRes.ok) {
          const alertsData = await alertsRes.json();
          setAlerts(alertsData.alerts || []);
        }
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [scanData]);

  // Update metrics and networks when scanData changes
  useEffect(() => {
    if (scanData) {
      setMetrics(scanData.summary);
      setNetworks(scanData.networks);
    }
  }, [scanData]);

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-cyan-900/20 via-blue-900/20 to-purple-900/20 border border-cyan-500/30 rounded-lg p-8 backdrop-blur-sm">
        <h2 className="text-3xl font-bold text-white mb-2">Security Operations Dashboard</h2>
        <p className="text-cyan-400">Real-time WiFi network assessment and threat analysis</p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total Networks"
          value={metrics.total}
          icon="📡"
          color="blue"
          description="Networks detected"
        />
        <MetricCard
          title="High Risk"
          value={metrics.high_risk}
          icon="🚨"
          color="red"
          description="Immediate action needed"
        />
        <MetricCard
          title="Medium Risk"
          value={metrics.medium_risk}
          icon="⚠️"
          color="yellow"
          description="Review recommended"
        />
        <MetricCard
          title="Low Risk"
          value={metrics.low_risk}
          icon="✅"
          color="green"
          description="Secure networks"
        />
      </div>

      {/* Charts and Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Chart */}
        <div className="lg:col-span-1">
          {risk_distribution.length > 0 && (
            <RiskChart data={risk_distribution} />
          )}
        </div>

        {/* Recent Alerts */}
        <div className="lg:col-span-2">
          <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
              <span>🔔</span>
              <span>Recent Security Alerts</span>
            </h3>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {alerts.length > 0 ? (
                alerts.slice(0, 5).map((alert, idx) => (
                  <AlertCard key={idx} alert={alert} index={idx} />
                ))
              ) : (
                <p className="text-gray-400 text-center py-8">No alerts at this time. Good security posture! ✨</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Network List */}
      <div className="bg-slate-800/30 border border-slate-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
          <span>📊</span>
          <span>Detected Networks</span>
        </h3>
        <NetworkList networks={networks} loading={loading && networks.length === 0} />
      </div>

      {/* Footer Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        <div className="bg-slate-800/20 border border-slate-700 rounded-lg p-6">
          <p className="text-gray-400 text-sm mb-2">Last Scan</p>
          <p className="text-white font-semibold">{scanData ? new Date(scanData.summary.timestamp).toLocaleTimeString() : 'Never'}</p>
        </div>
        <div className="bg-slate-800/20 border border-slate-700 rounded-lg p-6">
          <p className="text-gray-400 text-sm mb-2">Total Threats</p>
          <p className="text-white font-semibold">{alerts.length}</p>
        </div>
        <div className="bg-slate-800/20 border border-slate-700 rounded-lg p-6">
          <p className="text-gray-400 text-sm mb-2">Security Status</p>
          <p className="text-green-400 font-semibold" >🟢 Operational</p>
        </div>
      </div>
    </div>
  );
}
