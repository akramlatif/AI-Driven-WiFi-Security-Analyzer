# 🛡️ WiFi Security Analyzer - SOC Dashboard

A modern, professional Security Operations Center (SOC) dashboard for WiFi network security analysis with real-time threat detection and AI-driven prioritization.

## ✨ Features

### Dashboard
- 📊 Real-time security metrics and KPIs
- 🔴 Risk distribution visualization with charts
- 🚨 Live security alerts and threat timeline
- 📡 Network topology with threat indicators
- 📈 Trend analysis and historical data

### Network Scanner
- 🔍 Comprehensive WiFi network scanning
- 📊 AI-powered risk scoring
- 🎯 Threat prioritization
- ⚡ Real-time threat detection
- 🔐 Encryption analysis

### Password Analyzer
- 🔐 Password strength evaluation
- 📋 Weakness pattern detection
- 💡 Security recommendations
- 🎯 Policy hardening suggestions
- 📊 Estimated crack time calculation

### Traffic Analysis
- 📡 Network packet inspection
- 🔍 Anomaly detection
- 📊 Traffic pattern analysis
- 🚨 Suspicious behavior detection
- 📈 Real-time monitoring

### Alerts & Reporting
- ⚠️ Real-time security alerts
- 📄 Comprehensive security reports
- 📊 Detailed threat analysis
- 💾 Report generation and export
- 📧 Alert management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask backend API:**
   ```bash
   python backend.py
   ```
   The API will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   The dashboard will open at `http://localhost:3000`

## 📱 Dashboard Pages

### 1. **Dashboard** 📊
The main overview page with:
- Real-time metrics (Total Networks, High/Medium/Low Risk)
- Risk distribution chart
- Recent security alerts
- Detected networks list
- System status indicators

### 2. **Network Scanner** 🔍
- Scan nearby WiFi networks
- AI-powered risk scoring
- Real-time threat analysis
- Signal strength monitoring
- Encryption verification

### 3. **Password Analyzer** 🔐
- Test password strength
- Identify weakness patterns
- Get security recommendations
- Estimated crack time
- Detailed analysis breakdown

### 4. **Traffic Analysis** 📡
- Analyze network traffic
- Detect anomalies
- Monitor suspicious patterns
- Real-time packet inspection
- Behavioral analysis

### 5. **Alerts** ⚠️
- Real-time security alerts
- Filter by severity
- Alert timeline
- Threat details
- Response recommendations

### 6. **Reports** 📄
- Generate security reports
- Comprehensive analysis
- Threat summary
- Recommendations
- Download as markdown

## 🎨 UI/UX Highlights

### Professional SOC Design
- ✨ Dark theme optimized for security monitoring
- 🎯 Intuitive navigation and layout
- 📊 Rich data visualizations
- 🚨 Clear threat severity indicators
- 📈 Real-time metric updates

### Responsive Layout
- 💻 Desktop optimized
- 📱 Mobile responsive
- 🖥️ Tablet compatible
- ⚡ Fast performance

### Visual Indicators
- 🔴 Red - Critical/High risk
- 🟡 Yellow/Orange - Medium risk
- 🟢 Green - Low risk/Secure
- 🔵 Blue/Cyan - Info/Monitoring

## 🔌 API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `POST /api/scan-networks` - Scan and score networks
- `POST /api/analyze-password` - Analyze password strength
- `POST /api/analyze-traffic` - Analyze network traffic
- `GET /api/generate-alerts` - Get security alerts
- `GET /api/adaptive-insights` - Get adaptive learning insights
- `GET /api/risk-distribution` - Get risk chart data
- `POST /api/automation` - Run end-to-end assessment
- `GET /api/generate-report` - Generate security report

## 📁 Project Structure

```
.
├── frontend/                    # React dashboard
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Header.jsx
│   │   │   ├── MetricCard.jsx
│   │   │   ├── AlertCard.jsx
│   │   │   ├── NetworkList.jsx
│   │   │   └── RiskChart.jsx
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── NetworkScanner.jsx
│   │   │   ├── PasswordAnalyzer.jsx
│   │   │   ├── TrafficAnalysis.jsx
│   │   │   ├── AlertsPanel.jsx
│   │   │   └── Reports.jsx
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── src/                        # Python analyzer modules
│   └── analyzer/
│       ├── scanner.py
│       ├── risk_ai.py
│       ├── password_audit.py
│       ├── traffic_analysis.py
│       ├── alerts.py
│       └── ...
├── backend.py                  # Flask API server
├── requirements.txt            # Python dependencies
└── app.py                      # Original Streamlit app (optional)
```

## 🔐 Security Features

- ✅ Secure password evaluation
- ✅ Traffic anomaly detection
- ✅ Real-time threat monitoring
- ✅ AI-powered risk scoring
- ✅ Defensive behavior analysis
- ✅ Adaptive learning system
- ✅ Comprehensive reporting

## 📊 Technologies Used

### Frontend
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **Chart.js** - Data visualization
- **Vite** - Build tool

### Backend
- **Flask** - API framework
- **Flask-CORS** - CORS support
- **Pandas** - Data manipulation
- **scikit-learn** - ML models
- **joblib** - Model persistence

## ⚙️ Configuration

### Backend Configuration
Edit `backend.py` to configure:
- API host and port
- CORS settings
- Data paths

### Frontend Configuration
Edit `frontend/vite.config.js` to configure:
- Development server port
- Build output directory
- API proxy settings

## 🐛 Troubleshooting

### Backend not connecting
- Ensure Flask is running: `python backend.py`
- Check API status in dashboard header
- Verify CORS is enabled

### Frontend not loading
- Clear browser cache
- Check Node.js version: `node -v`
- Reinstall dependencies: `npm install`

### Data not showing
- Run a network scan first
- Check backend console for errors
- Verify sample data path exists

## 📝 License

This project is for authorized WiFi security assessments only. Use responsibly and legally.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📞 Support

For issues and questions, please refer to the main project documentation.

---

**Stay secure! 🛡️**
