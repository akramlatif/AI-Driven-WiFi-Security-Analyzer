from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

MODEL_PATH = Path("data/risk_model.joblib")
SEED_PATH = Path("data/network_risk_seed.csv")


SECURITY_PRIOR = {
    "OPEN": 0.95,
    "WEP": 0.9,
    "WPA": 0.75,
    "WPA2": 0.35,
    "WPA3": 0.15,
    "UNKNOWN": 0.6,
}


def _build_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "security",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                ["security_type"],
            ),
            (
                "numeric",
                Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]),
                ["signal_strength", "wps_enabled", "hidden_ssid", "known_vendor_risk"],
            ),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("clf", DecisionTreeClassifier(max_depth=5, random_state=42)),
        ]
    )


def _synthetic_seed() -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(42)
    securities = ["OPEN", "WEP", "WPA", "WPA2", "WPA3"]

    for _ in range(600):
        security = securities[rng.integers(0, len(securities))]
        signal = int(rng.integers(15, 95))
        wps = int(rng.integers(0, 2))
        hidden = int(rng.integers(0, 2))
        vendor_risk = int(rng.integers(0, 2))

        prior = SECURITY_PRIOR.get(security, 0.5)
        score = prior
        score += 0.12 if wps else 0
        score += 0.08 if hidden else 0
        score += 0.1 if vendor_risk else 0
        score += 0.05 if signal > 75 else 0
        label = 1 if score >= 0.65 else 0

        rows.append(
            {
                "security_type": security,
                "signal_strength": signal,
                "wps_enabled": wps,
                "hidden_ssid": hidden,
                "known_vendor_risk": vendor_risk,
                "high_risk": label,
            }
        )

    return pd.DataFrame(rows)


def _load_training_data() -> pd.DataFrame:
    if SEED_PATH.exists():
        return pd.read_csv(SEED_PATH)
    data = _synthetic_seed()
    SEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(SEED_PATH, index=False)
    return data


def load_or_train_model() -> Pipeline:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)

    train_df = _load_training_data()
    model = _build_pipeline()
    model.fit(train_df.drop(columns=["high_risk"]), train_df["high_risk"])

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def score_networks(network_df: pd.DataFrame) -> pd.DataFrame:
    model = load_or_train_model()
    frame = network_df.copy()

    required = ["signal_strength", "security_type", "wps_enabled", "hidden_ssid", "known_vendor_risk"]
    for col in required:
        if col not in frame.columns:
            frame[col] = 0

    probs = model.predict_proba(frame[required])[:, 1]
    frame["risk_score"] = (probs * 100).round(2)
    frame["risk_label"] = np.where(frame["risk_score"] >= 70, "High", np.where(frame["risk_score"] >= 40, "Medium", "Low"))
    return frame.sort_values(by=["risk_score", "signal_strength"], ascending=[False, False]).reset_index(drop=True)
