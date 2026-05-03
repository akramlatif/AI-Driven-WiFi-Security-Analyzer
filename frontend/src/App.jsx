import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import NetworkScanner from './pages/NetworkScanner';
import PasswordAnalyzer from './pages/PasswordAnalyzer';
import TrafficAnalysis from './pages/TrafficAnalysis';
import AlertsPanel from './pages/AlertsPanel';
import Reports from './pages/Reports';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [apiStatus, setApiStatus] = useState(false);
  const [scanData, setScanData] = useState(null);

  // Check API status
  useEffect(() => {
    const checkAPI = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/health');
        setApiStatus(response.ok);
      } catch (error) {
        setApiStatus(false);
      }
    };

    checkAPI();
    const interval = setInterval(checkAPI, 5000);
    return () => clearInterval(interval);
  }, []);

  const renderPage = () => {
    switch(currentPage) {
      case 'dashboard':
        return <Dashboard scanData={scanData} />;
      case 'scanner':
        return <NetworkScanner onScanComplete={setScanData} />;
      case 'password':
        return <PasswordAnalyzer />;
      case 'traffic':
        return <TrafficAnalysis />;
      case 'alerts':
        return <AlertsPanel />;
      case 'reports':
        return <Reports />;
      default:
        return <Dashboard scanData={scanData} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-gray-100">
      <Header 
        currentPage={currentPage} 
        onPageChange={setCurrentPage}
        apiStatus={apiStatus}
      />
      <main className="container mx-auto px-4 py-8">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
