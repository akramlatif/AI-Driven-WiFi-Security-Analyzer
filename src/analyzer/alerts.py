import pandas as pd

from .models import PasswordAuditResult, TrafficAnalysisResult


def generate_alerts(
    network_table: pd.DataFrame | None,
    password_result: PasswordAuditResult | None,
    traffic_result: TrafficAnalysisResult | None,
) -> list[dict[str, str]]:
    alerts: list[dict[str, str]] = []

    if network_table is not None and not network_table.empty:
        open_count = int((network_table["security_type"] == "OPEN").sum())
        wep_count = int((network_table["security_type"] == "WEP").sum())
        high_count = int((network_table["risk_label"] == "High").sum())

        if open_count > 0:
            alerts.append(
                {
                    "severity": "critical",
                    "message": f"Detected {open_count} open network(s). Enforce WPA2/WPA3 immediately.",
                }
            )
        if wep_count > 0:
            alerts.append(
                {
                    "severity": "critical",
                    "message": f"Detected {wep_count} WEP network(s). Migrate to WPA3 or WPA2-AES.",
                }
            )
        if high_count > 0:
            alerts.append(
                {
                    "severity": "high",
                    "message": f"{high_count} high-risk network(s) need urgent hardening.",
                }
            )

    if password_result is not None:
        if password_result.rating == "Weak":
            alerts.append(
                {
                    "severity": "high",
                    "message": "Password audit is weak. Update passphrases and apply policy enforcement.",
                }
            )
        elif password_result.rating == "Moderate":
            alerts.append(
                {
                    "severity": "medium",
                    "message": "Password audit is moderate. Increase complexity and length.",
                }
            )

    if traffic_result is not None:
        if traffic_result.status == "High risk":
            alerts.append(
                {
                    "severity": "high",
                    "message": "Traffic anomaly ratio is high. Investigate suspicious flows immediately.",
                }
            )
        elif traffic_result.status == "Moderate":
            alerts.append(
                {
                    "severity": "medium",
                    "message": "Moderate anomalies observed. Review protocol distribution and outliers.",
                }
            )

    if not alerts:
        alerts.append({"severity": "info", "message": "No urgent issues detected in this run."})

    return alerts
