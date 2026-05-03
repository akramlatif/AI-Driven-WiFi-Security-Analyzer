@echo off
REM WiFi Security Analyzer - SOC Dashboard Startup Script

echo.
echo 🛡️  WiFi Security Analyzer - Starting SOC Dashboard
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    exit /b 1
)

echo ✅ Python and Node.js found
echo.

REM Install/Update Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
echo ✅ Python dependencies installed
echo.

REM Install/Update frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
call npm install >nul 2>&1
echo ✅ Frontend dependencies installed
cd ..
echo.

REM Start backend
echo 🚀 Starting backend API on http://localhost:5000...
start "WiFi Analyzer Backend" python backend.py
timeout /t 2 /nobreak

REM Start frontend
echo 🚀 Starting frontend on http://localhost:3000...
cd frontend
start "WiFi Analyzer Frontend" npm run dev
cd ..

echo.
echo ==================================================
echo ✅ WiFi Security Analyzer is starting!
echo.
echo 📍 Dashboard: http://localhost:3000
echo 🔗 API: http://localhost:5000
echo.
echo Close terminal windows to stop services
echo ==================================================
