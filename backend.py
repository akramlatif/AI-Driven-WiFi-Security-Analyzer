from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import sys
import pandas as pd
import json
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from analyzer.scanner import scan_networks, to_frame
from analyzer.risk_ai import score_networks
from analyzer.alerts import generate_alerts
from analyzer.password_audit import audit_password
from analyzer.traffic_analysis import analyze_packet_features
from analyzer.automation import run_end_to_end_assessment
from analyzer.adaptive_learning import get_adaptive_insights, get_history
from analyzer.reporting import build_markdown_report

app = Flask(__name__)
CORS(app)

# Store session state
session_storage = {
    "network_scored": pd.DataFrame(),
    "password_result": None,
    "traffic_result": None,
    "traffic_table": pd.DataFrame(),
    "alerts": [],
    "adaptive_insights": [],
    "blocklist_preview": [],
    "automation_result": None,
}


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "WiFi Security Analyzer backend running"})


@app.route("/api/scan-networks", methods=["POST"])
def scan_and_score_networks():
    """Scan networks and provide risk scoring"""
    try:
        data = request.json
        simulate = data.get("simulate", True)
        
        records = scan_networks(simulate=simulate)
        network_df = to_frame(records)
        scored_df = score_networks(network_df)
        
        session_storage["network_scored"] = scored_df
        
        # Format for frontend
        networks = []
        for idx, row in scored_df.iterrows():
            networks.append({
                "id": idx,
                "ssid": row.get("ssid", "N/A"),
                "signal": row.get("signal_strength", 0),
                "encryption": row.get("encryption", "Unknown"),
                "risk_score": round(float(row.get("risk_score", 0)), 2),
                "risk_label": row.get("risk_label", "Unknown"),
                "channel": row.get("channel", "N/A"),
                "threat_count": len(row.get("threats", [])) if "threats" in row else 0,
            })
        
        # Calculate summary
        high = len([n for n in networks if n["risk_label"] == "High"])
        medium = len([n for n in networks if n["risk_label"] == "Medium"])
        low = len([n for n in networks if n["risk_label"] == "Low"])
        
        return jsonify({
            "success": True,
            "networks": networks,
            "summary": {
                "total": len(networks),
                "high_risk": high,
                "medium_risk": medium,
                "low_risk": low,
                "timestamp": datetime.now().isoformat(),
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/analyze-password", methods=["POST"])
def analyze_password():
    """Analyze password strength"""
    try:
        data = request.json
        password = data.get("password", "")
        
        if not password:
            return jsonify({"success": False, "error": "Password required"}), 400
        
        result = audit_password(password)
        session_storage["password_result"] = result
        
        return jsonify({
            "success": True,
            "password_analysis": result
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/analyze-traffic", methods=["POST"])
def analyze_traffic():
    """Analyze network traffic"""
    try:
        data = request.json
        
        # This would normally process actual traffic data
        # For now, using sample data
        result = analyze_packet_features()
        session_storage["traffic_result"] = result
        
        return jsonify({
            "success": True,
            "traffic_analysis": result
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/generate-alerts", methods=["GET"])
def get_alerts():
    """Get security alerts"""
    try:
        alerts = generate_alerts(
            session_storage["network_scored"],
            session_storage["password_result"],
            session_storage["traffic_result"],
        )
        
        session_storage["alerts"] = alerts
        
        # Format alerts for dashboard
        formatted_alerts = []
        for alert in alerts:
            formatted_alerts.append({
                "id": len(formatted_alerts),
                "type": alert.get("type", "info"),
                "severity": alert.get("severity", "low"),
                "message": alert.get("message", ""),
                "timestamp": datetime.now().isoformat(),
            })
        
        return jsonify({
            "success": True,
            "alerts": formatted_alerts,
            "total": len(formatted_alerts),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/adaptive-insights", methods=["GET"])
def get_insights():
    """Get adaptive learning insights"""
    try:
        insights = get_adaptive_insights(session_storage["network_scored"])
        history = get_history()
        
        return jsonify({
            "success": True,
            "insights": insights if insights else [],
            "history": history if history else [],
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/risk-distribution", methods=["GET"])
def get_risk_distribution():
    """Get risk score distribution for charts"""
    try:
        if session_storage["network_scored"].empty:
            return jsonify({
                "success": True,
                "distribution": []
            })
        
        df = session_storage["network_scored"]
        distribution = [
            {"label": "High Risk", "count": int((df["risk_label"] == "High").sum()), "color": "#ef4444"},
            {"label": "Medium Risk", "count": int((df["risk_label"] == "Medium").sum()), "color": "#f59e0b"},
            {"label": "Low Risk", "count": int((df["risk_label"] == "Low").sum()), "color": "#10b981"},
        ]
        
        return jsonify({
            "success": True,
            "distribution": distribution
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/automation", methods=["POST"])
def run_automation():
    """Run end-to-end assessment"""
    try:
        result = run_end_to_end_assessment()
        session_storage["automation_result"] = result
        
        return jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/generate-report", methods=["GET"])
def generate_report():
    """Generate security report"""
    try:
        if session_storage["network_scored"].empty:
            return jsonify({"success": False, "error": "No scan data available"}), 400
        
        report = build_markdown_report(session_storage["network_scored"])
        
        return jsonify({
            "success": True,
            "report": report,
            "timestamp": datetime.now().isoformat(),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
