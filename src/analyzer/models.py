from dataclasses import dataclass, field
from typing import List, Optional

import pandas as pd


@dataclass
class NetworkRecord:
    """Data model for a single discovered network."""

    ssid: str
    bssid: str
    signal_strength: int
    security_type: str
    channel: str
    wps_enabled: int = 0
    hidden_ssid: int = 0
    known_vendor_risk: int = 0


@dataclass
class PasswordAuditResult:
    """Data model for password audit findings."""

    score: int
    rating: str
    findings: List[str]
    recommendations: List[str]


@dataclass
class TrafficAnalysisResult:
    """Data model for traffic analysis findings."""

    status: str
    anomaly_ratio: float
    anomaly_rows: int
    total_rows: int


@dataclass
class AutomationResult:
    """Data model for the end-to-end automation output."""

    network_table: pd.DataFrame
    alerts: List[dict]
    adaptive_insights: List[str]
    password_result: Optional[PasswordAuditResult] = None
    traffic_table: Optional[pd.DataFrame] = None
    traffic_result: Optional[TrafficAnalysisResult] = None


@dataclass
class AssessmentRecord:
    """Data model for a single historical assessment record."""

    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    avg_risk_score: float
    password_score: Optional[int] = None
    anomaly_ratio: Optional[float] = None
    timestamp: str = field(default_factory=lambda: pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))

