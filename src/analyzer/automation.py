import pandas as pd

from .adaptive_learning import (
    append_assessment_history,
    get_adaptive_insights,
    get_history,
)
from .alerts import generate_alerts
from .models import AssessmentRecord, AutomationResult
from .password_audit import audit_password
from .risk_ai import score_networks
from .scanner import scan_networks, to_frame
from .traffic_analysis import analyze_packet_features


def run_end_to_end_assessment(
    simulate_scan: bool = True,
    password_sample: str | None = None,
    packet_df: pd.DataFrame | None = None,
) -> AutomationResult:
    """
    Runs a full, automated assessment and returns a structured result.

    Args:
        simulate_scan: Whether to use sample network data.
        password_sample: An optional password to include in the audit.
        packet_df: An optional DataFrame with traffic data for analysis.

    Returns:
        An AutomationResult object containing all findings.
    """
    records = scan_networks(simulate=simulate_scan)
    network_df = to_frame(records)
    scored = score_networks(network_df)

    password_result = audit_password(password_sample) if password_sample else None

    traffic_table = pd.DataFrame()
    traffic_result = None
    if packet_df is not None and not packet_df.empty:
        traffic_table, traffic_result = analyze_packet_features(packet_df)

    alerts = generate_alerts(scored, password_result, traffic_result)

    high = int((scored["risk_label"] == "High").sum())
    med = int((scored["risk_label"] == "Medium").sum())
    low = int((scored["risk_label"] == "Low").sum())
    avg_risk = float(scored["risk_score"].mean()) if not scored.empty else 0.0

    history_record = AssessmentRecord(
        high_risk_count=high,
        medium_risk_count=med,
        low_risk_count=low,
        avg_risk_score=avg_risk,
        password_score=password_result.score if password_result else None,
        anomaly_ratio=traffic_result.anomaly_ratio if traffic_result else None,
    )
    append_assessment_history(history_record)

    adaptive_insights = get_adaptive_insights(get_history())

    return AutomationResult(
        network_table=scored,
        password_result=password_result,
        traffic_table=traffic_table,
        traffic_result=traffic_result,
        alerts=alerts,
        adaptive_insights=adaptive_insights,
    )

