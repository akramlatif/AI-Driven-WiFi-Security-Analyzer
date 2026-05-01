import numpy as np
import pandas as pd

def generate_suspicious_samples(sample_count: int = 100) -> pd.DataFrame:
    """
    Generates a synthetic dataset mimicking suspicious network traffic patterns.

    Args:
        sample_count: The number of suspicious records to generate.

    Returns:
        A DataFrame with suspicious traffic data.
    """
    data = []

    # 1. Port Scanning Simulation (30% of samples)
    scan_count = int(sample_count * 0.3)
    for i in range(scan_count):
        data.append({
            "protocol": "TCP",
            "frame_len": np.random.randint(40, 80),
            "delta_time": np.random.uniform(0.001, 0.05),
            "src_port": np.random.randint(49152, 65535),
            "dst_port": 80 + i,  # Sequential port access
        })

    # 2. Large Packet Payloads (30% of samples)
    large_packet_count = int(sample_count * 0.3)
    for _ in range(large_packet_count):
        data.append({
            "protocol": "UDP",
            "frame_len": np.random.randint(1500, 9000),  # Jumbo frames
            "delta_time": np.random.uniform(0.1, 0.5),
            "src_port": np.random.randint(49152, 65535),
            "dst_port": np.random.randint(1024, 49151),
        })

    # 3. Unusual Protocol / Port Combo (20% of samples)
    unusual_count = int(sample_count * 0.2)
    for _ in range(unusual_count):
        data.append({
            "protocol": "ICMP",
            "frame_len": np.random.randint(28, 100),
            "delta_time": np.random.uniform(0.01, 0.2),
            "src_port": 0, # ICMP doesn't use ports like TCP/UDP
            "dst_port": 0,
        })

    # 4. Rapid, small packets (20% of samples)
    rapid_count = sample_count - len(data)
    for _ in range(rapid_count):
        data.append({
            "protocol": "TCP",
            "frame_len": np.random.randint(20, 40),
            "delta_time": np.random.uniform(0.0001, 0.005),
            "src_port": np.random.randint(49152, 65535),
            "dst_port": 443,
        })

    return pd.DataFrame(data)
