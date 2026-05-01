import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .models import TrafficAnalysisResult


DEFAULT_COLUMNS = ["protocol", "frame_len", "delta_time", "src_port", "dst_port"]


def analyze_packet_features(packet_df: pd.DataFrame) -> tuple[pd.DataFrame, TrafficAnalysisResult]:
    if packet_df.empty:
        return packet_df, TrafficAnalysisResult(0.0, 0, 0, "No data")

    df = packet_df.copy()

    # Ensure all expected features exist so the analysis pipeline stays stable.
    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            if col == "protocol":
                df[col] = "unknown"
            else:
                df[col] = 0.0

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["frame_len", "delta_time", "src_port", "dst_port"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["protocol"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "detector",
                IsolationForest(
                    n_estimators=150,
                    contamination=0.08,
                    random_state=42,
                ),
            ),
        ]
    )

    model.fit(df[DEFAULT_COLUMNS])
    labels = model.named_steps["detector"].predict(model.named_steps["preprocessor"].transform(df[DEFAULT_COLUMNS]))
    scores = model.named_steps["detector"].decision_function(
        model.named_steps["preprocessor"].transform(df[DEFAULT_COLUMNS])
    )

    out = df.copy()
    out["anomaly_label"] = ["anomaly" if x == -1 else "normal" for x in labels]
    out["anomaly_score"] = scores

    anomaly_rows = int((out["anomaly_label"] == "anomaly").sum())
    total_rows = int(len(out))
    anomaly_ratio = (anomaly_rows / total_rows) if total_rows else 0.0
    status = "High risk" if anomaly_ratio > 0.2 else "Moderate" if anomaly_ratio > 0.08 else "Low"

    result = TrafficAnalysisResult(
        anomaly_ratio=round(anomaly_ratio, 4),
        anomaly_rows=anomaly_rows,
        total_rows=total_rows,
        status=status,
    )
    return out, result
