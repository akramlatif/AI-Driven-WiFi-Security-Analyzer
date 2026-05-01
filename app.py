from pathlib import Path
import sys

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from analyzer.adaptive_learning import get_adaptive_insights, get_history
from analyzer.alerts import generate_alerts
from analyzer.automation import run_end_to_end_assessment
from analyzer.defensive_behavior import generate_benign_behavior_samples
from analyzer.password_audit import (
    audit_password,
    generate_defensive_blocklist,
    password_pattern_features,
)
from analyzer.reporting import build_markdown_report, write_report, MarkdownReportGenerator
from analyzer.risk_ai import score_networks
from analyzer.scanner import scan_networks, to_frame
from analyzer.traffic_analysis import analyze_packet_features
from analyzer.suspicious_behavior import generate_suspicious_samples


st.set_page_config(page_title="AI-Driven WiFi Security Analyzer", layout="wide")
st.title("AI-Driven WiFi Security Analyzer")
st.caption("Defensive lab tool for authorized WiFi security assessments with AI-driven prioritization")

st.warning(
    "Use only on networks you own or have explicit permission to assess. "
    "This app does not perform unauthorized intrusion, cracking, or stealth-evasion operations."
)

if "network_scored" not in st.session_state:
    st.session_state.network_scored = pd.DataFrame()
if "password_result" not in st.session_state:
    st.session_state.password_result = None
if "traffic_result" not in st.session_state:
    st.session_state.traffic_result = None
if "traffic_table" not in st.session_state:
    st.session_state.traffic_table = pd.DataFrame()
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "adaptive_insights" not in st.session_state:
    st.session_state.adaptive_insights = []
if "blocklist_preview" not in st.session_state:
    st.session_state.blocklist_preview = []
if "automation_result" not in st.session_state:
    st.session_state.automation_result = None


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Network Scanning & Risk",
        "Password Pattern Intelligence",
        "Traffic Anomaly Analysis",
        "Automation",
        "Alerts & Adaptive Learning",
        "Reporting",
    ]
)

with tab1:
    st.subheader("Nearby WiFi Network Assessment")
    simulate = st.checkbox("Use sample data (recommended for demo)", value=True)

    if st.button("Scan and Prioritize Networks", type="primary"):
        records = scan_networks(simulate=simulate)
        network_df = to_frame(records)
        scored_df = score_networks(network_df)
        st.session_state.network_scored = scored_df

    if not st.session_state.network_scored.empty:
        st.dataframe(st.session_state.network_scored, use_container_width=True)

        high = int((st.session_state.network_scored["risk_label"] == "High").sum())
        medium = int((st.session_state.network_scored["risk_label"] == "Medium").sum())
        low = int((st.session_state.network_scored["risk_label"] == "Low").sum())

        c1, c2, c3 = st.columns(3)
        c1.metric("High Risk", high)
        c2.metric("Medium Risk", medium)
        c3.metric("Low Risk", low)

        st.session_state.alerts = generate_alerts(
            st.session_state.network_scored,
            st.session_state.password_result,
            st.session_state.traffic_result,
        )

with tab2:
    st.subheader("Password Weakness Analysis (Defensive AI)")
    st.write(
        "Evaluate passphrase quality and weak patterns. "
        "AI-assisted blocklist generation is used for policy hardening, not cracking."
    )

    sample_password = st.text_input("Test password", type="password", placeholder="Enter sample passphrase")
    seed_terms = st.text_input(
        "Policy blocklist seed terms (comma-separated)",
        placeholder="company,teamname,campus",
    )
    if st.button("Analyze Password"):
        if sample_password:
            result = audit_password(sample_password)
            st.session_state.password_result = result
            feature_map = password_pattern_features(sample_password)
            st.json(feature_map)

            if seed_terms.strip():
                terms = [item.strip() for item in seed_terms.split(",") if item.strip()]
                st.session_state.blocklist_preview = generate_defensive_blocklist(terms, max_terms=60)

            st.session_state.alerts = generate_alerts(
                st.session_state.network_scored,
                st.session_state.password_result,
                st.session_state.traffic_result,
            )
        else:
            st.info("Enter a password to analyze.")

    result = st.session_state.password_result
    if result:
        st.metric("Score", f"{result.score}/100")
        st.metric("Rating", result.rating)
        st.write("Findings")
        for finding in result.findings:
            st.write(f"- {finding}")
        st.write("Recommendations")
        for item in result.recommendations:
            st.write(f"- {item}")

    if st.session_state.blocklist_preview:
        st.write("Generated Defensive Blocklist Preview")
        st.code("\n".join(st.session_state.blocklist_preview[:40]))

with tab3:
    st.subheader("Traffic Pattern Anomaly Detection")
    st.write("Upload CSV with packet-level features: protocol, frame_len, delta_time, src_port, dst_port")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Generate Benign Baseline Dataset"):
            baseline_df = generate_benign_behavior_samples(sample_count=300)
            st.session_state.traffic_table, st.session_state.traffic_result = analyze_packet_features(baseline_df)
            st.success("Generated and analyzed synthetic benign behavior dataset.")

    with c2:
        if st.button("Generate Suspicious Activity Dataset", type="primary"):
            suspicious_df = generate_suspicious_samples(sample_count=100)
            st.session_state.traffic_table, st.session_state.traffic_result = analyze_packet_features(suspicious_df)
            st.success("Generated and analyzed synthetic suspicious activity dataset.")

    upload = st.file_uploader("Upload packet feature CSV", type=["csv"])
    if upload is not None:
        packet_df = pd.read_csv(upload)
        analyzed_df, traffic_result = analyze_packet_features(packet_df)
        st.session_state.traffic_table = analyzed_df
        st.session_state.traffic_result = traffic_result
        st.session_state.alerts = generate_alerts(
            st.session_state.network_scored,
            st.session_state.password_result,
            st.session_state.traffic_result,
        )

    traffic_result = st.session_state.traffic_result
    if traffic_result:
        col1, col2, col3 = st.columns(3)
        col1.metric("Anomaly Ratio", f"{traffic_result.anomaly_ratio:.2%}")
        col2.metric("Anomalies", traffic_result.anomaly_rows)
        col3.metric("Status", traffic_result.status)

        st.dataframe(st.session_state.traffic_table.head(100), use_container_width=True)

with tab4:
    st.subheader("End-to-End Automation")
    st.write("Run scanning, AI prioritization, password check, traffic analysis, and history update in one click.")

    automate_sim = st.checkbox("Automation uses sample scan data", value=True)
    automate_password = st.text_input(
        "Optional password sample for automation",
        type="password",
        placeholder="Leave empty to skip",
    )

    if st.button("Run Full Assessment Automation", type="primary"):
        packet_df = st.session_state.traffic_table if not st.session_state.traffic_table.empty else None
        auto_result = run_end_to_end_assessment(
            simulate_scan=automate_sim,
            password_sample=automate_password if automate_password else None,
            packet_df=packet_df,
        )

        st.session_state.network_scored = auto_result.network_table
        st.session_state.password_result = auto_result.password_result
        st.session_state.traffic_table = auto_result.traffic_table
        st.session_state.traffic_result = auto_result.traffic_result
        st.session_state.alerts = auto_result.alerts
        st.session_state.adaptive_insights = get_adaptive_insights(get_history())
        st.session_state.automation_result = auto_result  # Save the full result
        st.success("Automated assessment completed.")

    if st.session_state.network_scored is not None and not st.session_state.network_scored.empty:
        st.dataframe(st.session_state.network_scored.head(10), use_container_width=True)

with tab5:
    st.subheader("Real-Time Alerts and Adaptive Learning")
    if not st.session_state.alerts:
        st.session_state.alerts = generate_alerts(
            st.session_state.network_scored,
            st.session_state.password_result,
            st.session_state.traffic_result,
        )

    for alert in st.session_state.alerts:
        sev = alert.get("severity", "info")
        msg = alert.get("message", "")
        if sev == "critical":
            st.error(msg)
        elif sev == "high":
            st.warning(msg)
        elif sev == "medium":
            st.info(msg)
        else:
            st.success(msg)

    history_df = get_history()
    if not history_df.empty:
        st.write("Historical trend (average risk score)")
        chart_df = history_df[["timestamp", "avg_risk_score"]].copy()
        chart_df["avg_risk_score"] = pd.to_numeric(chart_df["avg_risk_score"], errors="coerce")
        st.line_chart(chart_df.set_index("timestamp"))

        st.session_state.adaptive_insights = get_adaptive_insights(history_df)
        st.write("Adaptive AI insights")
        for insight in st.session_state.adaptive_insights:
            st.write(f"- {insight}")
    else:
        st.info("No history yet. Run automation at least once to build adaptive trends.")

with tab6:
    st.subheader("Generate Assessment Report")
    st.write("Create a markdown report summarizing findings and hardening recommendations.")

    if st.button("Build and Save Report", type="primary"):
        if st.session_state.automation_result:
            reporter = MarkdownReportGenerator()
            report = reporter.build(st.session_state.automation_result)
            report_path = reporter.write(report)
            st.success(f"Report saved: {report_path}")
            st.code(report[:3000], language="markdown")
        else:
            st.warning("Please run the full assessment automation first to generate a result.")
