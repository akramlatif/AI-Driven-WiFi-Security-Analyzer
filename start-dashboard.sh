#!/bin/bash

# WiFi Security Analyzer - SOC Dashboard Startup Script

echo "🛡️  WiFi Security Analyzer - Starting SOC Dashboard"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Install/Update Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Python dependencies installed"
echo ""

# Install/Update frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install --silent
echo "✅ Frontend dependencies installed"
cd ..
echo ""

# Start backend
echo "🚀 Starting backend API on http://localhost:5000..."
python backend.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
sleep 2

# Start frontend
echo "🚀 Starting frontend on http://localhost:3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "=================================================="
echo "✅ WiFi Security Analyzer is running!"
echo ""
echo "📍 Dashboard: http://localhost:3000"
echo "🔗 API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================================="

# Wait for interrupt
wait
