from datetime import datetime
from pathlib import Path

import pandas as pd

from .models import AssessmentRecord

HISTORY_PATH = Path("data/assessment_history.csv")


def append_assessment_history(record: AssessmentRecord) -> Path:
    """
    Appends a new assessment record to the history CSV.

    Args:
        record: The AssessmentRecord object to append.

    Returns:
        The path to the updated history file.
    """
    row = {
        "timestamp": record.timestamp,
        "high_risk_count": record.high_risk_count,
        "medium_risk_count": record.medium_risk_count,
        "low_risk_count": record.low_risk_count,
        "avg_risk_score": round(record.avg_risk_score, 2),
        "password_score": record.password_score if record.password_score is not None else "",
        "anomaly_ratio": round(record.anomaly_ratio, 4) if record.anomaly_ratio is not None else "",
    }

    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if HISTORY_PATH.exists():
        df = pd.read_csv(HISTORY_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(HISTORY_PATH, index=False)
    return HISTORY_PATH



def get_history() -> pd.DataFrame:
    if HISTORY_PATH.exists():
        return pd.read_csv(HISTORY_PATH)
    return pd.DataFrame(
        columns=[
            "timestamp",
            "high_risk_count",
            "medium_risk_count",
            "low_risk_count",
            "avg_risk_score",
            "password_score",
            "anomaly_ratio",
        ]
    )


def get_adaptive_insights(history_df: pd.DataFrame) -> list[str]:
    if history_df.empty or len(history_df) < 2:
        return ["Adaptive insights will appear after multiple assessment runs."]

    insights: list[str] = []
    recent = history_df.tail(5).copy()

    if "avg_risk_score" in recent.columns:
        trend = recent["avg_risk_score"].astype(float).diff().mean()
        if trend > 1.0:
            insights.append("Average network risk is trending upward. Prioritize remediation this week.")
        elif trend < -1.0:
            insights.append("Average network risk is improving over recent runs.")

    if "anomaly_ratio" in recent.columns and recent["anomaly_ratio"].astype(str).str.strip().ne("").any():
        anom = pd.to_numeric(recent["anomaly_ratio"], errors="coerce").dropna()
        if not anom.empty and anom.mean() > 0.12:
            insights.append("Traffic anomaly baseline is elevated. Increase monitoring and segmentation.")

    if "password_score" in recent.columns and recent["password_score"].astype(str).str.strip().ne("").any():
        pwd = pd.to_numeric(recent["password_score"], errors="coerce").dropna()
        if not pwd.empty and pwd.mean() < 65:
            insights.append("Password hygiene remains weak. Enforce stronger password policy and MFA.")

    return insights or ["No adverse trend detected in recent assessments."]
