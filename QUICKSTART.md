# 🚀 Quick Start Guide - SOC Dashboard

## What's New? 🎉

Your WiFi Security Analyzer now has a **professional SOC (Security Operations Center) dashboard** with:

- ✨ **Modern UI** - Dark theme optimized for security monitoring
- 📊 **Real-time Metrics** - Live threat indicators and KPIs
- 📈 **Rich Visualizations** - Charts, graphs, and data displays
- 🚨 **Alert Management** - Real-time security alerts and timeline
- 📡 **Network Analysis** - Beautiful network scanning interface
- 🔐 **Password Audit** - Enhanced password strength analyzer
- 📄 **Reports** - Generate comprehensive security assessments
- ⚡ **Fast & Responsive** - Optimized performance across devices

## Installation & Setup

### Option 1: Automatic Setup (Recommended) 🤖

#### On Linux/macOS:
```bash
chmod +x start-dashboard.sh
./start-dashboard.sh
```

#### On Windows:
```bash
start-dashboard.bat
```

This will automatically:
1. Install Python dependencies
2. Install Node.js dependencies
3. Start the Flask backend
4. Start the React frontend

### Option 2: Manual Setup

#### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Start Backend
```bash
python backend.py
```
Should see: `Running on http://0.0.0.0:5000`

#### Step 3: Start Frontend (New terminal)
```bash
cd frontend
npm install
npm run dev
```
Should see: `VITE v5.0.x ready in XXX ms`

## Accessing the Dashboard

- **Dashboard URL**: http://localhost:3000
- **API Endpoint**: http://localhost:5000
- **API Status**: Check the top right corner (green = connected)

## Dashboard Features

### 📊 Dashboard (Home)
- View real-time security metrics
- Risk distribution chart
- Recent alerts and threats
- Network summary statistics

### 🔍 Network Scanner
- Scan WiFi networks in your area
- View AI-powered risk scores
- See threat details and encryption info
- Real-time signal strength monitoring

### 🔐 Password Analyzer
- Test password strength
- Get security recommendations
- Identify weakness patterns
- Estimate crack time

### 📡 Traffic Analysis
- Analyze network packet data
- Detect anomalous patterns
- Monitor suspicious behavior

### ⚠️ Alerts
- View real-time security alerts
- Filter by severity level
- See alert timeline
- Detailed threat descriptions

### 📄 Reports
- Generate comprehensive security reports
- Detailed threat analysis
- Download as markdown files

## Project Structure

```
AI-Driven-WiFi-Security-Analyzer/
├── frontend/               # React Dashboard (NEW!)
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Dashboard pages
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── backend.py             # Flask API (NEW!)
├── requirements.txt       # Updated with Flask
├── start-dashboard.sh     # Auto startup script
├── start-dashboard.bat    # Windows startup script
└── DASHBOARD_README.md    # Full documentation
```

## Key Files Explained

### `backend.py`
- Flask API server
- Connects to existing analyzer modules
- Exposes endpoints for the frontend
- Handles CORS for frontend requests

### `frontend/`
- React-based web interface
- Modern SOC dashboard design
- All interactive features
- Tailwind CSS styling

### `start-dashboard.sh` / `start-dashboard.bat`
- One-click setup and startup
- Installs dependencies automatically
- Starts both backend and frontend

## Common Commands

### Development
```bash
# Start frontend only
cd frontend && npm run dev

# Start backend only
python backend.py

# Build frontend for production
cd frontend && npm run build
```

### Troubleshooting
```bash
# Force dependency reinstall
rm -rf frontend/node_modules
cd frontend && npm install

# Check if ports are in use
netstat -an | grep 3000    # Frontend
netstat -an | grep 5000    # Backend

# Kill processes on ports (Linux/Mac)
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

## Configuration

### Change Frontend Port
Edit `frontend/vite.config.js`:
```javascript
server: {
  port: 3001,  // Change here
}
```

### Change Backend Port
Edit `backend.py`:
```python
if __name__ == "__main__":
    app.run(port=5001)  # Change here
```

## Browser Compatibility

- ✅ Chrome/Brave 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## Performance Tips

1. **Use Sample Data** - Check "Use sample data" in Network Scanner for faster demo
2. **Browser DevTools** - Press F12 to open dev tools and check console
3. **Clear Cache** - Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
4. **Check Network** - Use DevTools Network tab to debug API calls

## Next Steps

1. Start the dashboard using auto setup or manual steps
2. Navigate to http://localhost:3000
3. Check API status (green indicator top-right)
4. Click "🔍 Network Scanner" to start scanning
5. View results on the Dashboard
6. Explore other features!

## Need Help?

### Dashboard won't load?
- Check if frontend is running: http://localhost:3000
- Check browser console (F12) for errors
- Try clearing cache: Ctrl+Shift+Delete

### API not connecting?
- Check if backend is running: python backend.py
- Check if port 5000 is available
- Look for errors in backend console

### Dependencies not installing?
- Ensure Python 3.8+ and Node.js 16+ are installed
- Try: `pip install --upgrade pip`
- Try: `npm install -g npm@latest`

## Features Comparison

| Feature | Before | After |
|---------|--------|-------|
| Interface | Streamlit | Modern React |
| Design | Basic | Professional SOC |
| Real-time | Partial | Full |
| Charts | Basic | Advanced (Chart.js) |
| Mobile | Limited | Fully Responsive |
| Performance | Slower | Optimized |
| Customization | Limited | Highly Customizable |

---

**🎉 Enjoy your new professional SOC dashboard!**

For full documentation, see `DASHBOARD_README.md`
