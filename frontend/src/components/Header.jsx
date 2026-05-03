import React, { useState } from 'react';

export default function Header({ currentPage, onPageChange, apiStatus }) {
  const [isOpen, setIsOpen] = useState(false);

  const menuItems = [
    { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
    { id: 'scanner', label: '🔍 Network Scanner', icon: '🔍' },
    { id: 'password', label: '🔐 Password Audit', icon: '🔐' },
    { id: 'traffic', label: '📡 Traffic Analysis', icon: '📡' },
    { id: 'alerts', label: '⚠️ Alerts', icon: '⚠️' },
    { id: 'reports', label: '📄 Reports', icon: '📄' },
  ];

  return (
    <header className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border-b border-cyan-900/30 sticky top-0 z-50 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg blur opacity-75 animate-pulse"></div>
              <div className="relative bg-slate-900 px-3 py-2 rounded-lg">
                <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                  🛡️
                </span>
              </div>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">WiFi Security Analyzer</h1>
              <p className="text-xs text-cyan-400">SOC Dashboard</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {menuItems.map(item => (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`px-4 py-2 rounded-lg transition-all duration-200 font-medium ${
                  currentPage === item.id
                    ? 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/50'
                    : 'text-gray-400 hover:text-cyan-400 hover:bg-slate-700/50'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </button>
            ))}
          </nav>

          {/* API Status & Mobile Menu */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${apiStatus ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
              <span className="text-xs text-gray-400">{apiStatus ? 'Connected' : 'Offline'}</span>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 hover:bg-slate-700 rounded-lg"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <nav className="md:hidden pb-4 space-y-2">
            {menuItems.map(item => (
              <button
                key={item.id}
                onClick={() => {
                  onPageChange(item.id);
                  setIsOpen(false);
                }}
                className={`w-full text-left px-4 py-2 rounded-lg transition-all duration-200 ${
                  currentPage === item.id
                    ? 'bg-cyan-600/20 text-cyan-400 border border-cyan-500/50'
                    : 'text-gray-400 hover:text-cyan-400 hover:bg-slate-700/50'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </button>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
