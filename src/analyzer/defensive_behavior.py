import numpy as np
import pandas as pd


def generate_benign_behavior_samples(sample_count: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    protocols = ["TLS", "TCP", "UDP", "DNS", "HTTP"]
    weights = np.array([0.38, 0.25, 0.18, 0.12, 0.07])

    df = pd.DataFrame(
        {
            "protocol": rng.choice(protocols, size=sample_count, p=weights),
            "frame_len": np.clip(rng.normal(720, 180, sample_count), 60, 1514).round(0),
            "delta_time": np.clip(rng.exponential(0.12, sample_count), 0.001, 3.0).round(4),
            "src_port": rng.choice([53, 80, 123, 443, 51522, 52001], size=sample_count),
            "dst_port": rng.choice([53, 80, 123, 443, 8080], size=sample_count),
        }
    )

    return df
