import platform
import re
import subprocess
from typing import Iterable

from .models import NetworkRecord


SECURITY_MAP = {
    "open": "OPEN",
    "none": "OPEN",
    "wep": "WEP",
    "wpa": "WPA",
    "wpa2": "WPA2",
    "wpa3": "WPA3",
}


def _normalize_security(raw: str) -> str:
    text = raw.lower()
    for key, value in SECURITY_MAP.items():
        if key in text:
            return value
    return "UNKNOWN"


def _safe_run(command: list[str]) -> str:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return result.stdout or ""
    except FileNotFoundError:
        return ""


def _parse_windows_netsh(output: str) -> list[NetworkRecord]:
    records: list[NetworkRecord] = []
    ssid_pattern = re.compile(r"^SSID\s+\d+\s*:\s*(.*)$")
    bssid_pattern = re.compile(r"^BSSID\s+\d+\s*:\s*(.*)$")
    signal_pattern = re.compile(r"^Signal\s*:\s*(\d+)%$")
    channel_pattern = re.compile(r"^Channel\s*:\s*(.*)$")
    auth_pattern = re.compile(r"^Authentication\s*:\s*(.*)$")

    current: dict[str, str] = {}
    for line in output.splitlines():
        text = line.strip()
        if not text:
            continue

        ssid_match = ssid_pattern.match(text)
        if ssid_match:
            if current:
                records.append(
                    NetworkRecord(
                        ssid=current.get("ssid", "<hidden>"),
                        bssid=current.get("bssid", "N/A"),
                        signal_strength=int(current.get("signal", "0")),
                        security_type=_normalize_security(current.get("auth", "unknown")),
                        channel=current.get("channel", "?"),
                        hidden_ssid=1 if current.get("ssid", "") == "" else 0,
                    )
                )
            current = {"ssid": ssid_match.group(1).strip()}
            continue

        for pattern, key in (
            (bssid_pattern, "bssid"),
            (signal_pattern, "signal"),
            (channel_pattern, "channel"),
            (auth_pattern, "auth"),
        ):
            match = pattern.match(text)
            if match and key not in current:
                current[key] = match.group(1).strip()
                break

    if current:
        records.append(
            NetworkRecord(
                ssid=current.get("ssid", "<hidden>"),
                bssid=current.get("bssid", "N/A"),
                signal_strength=int(current.get("signal", "0")),
                security_type=_normalize_security(current.get("auth", "unknown")),
                channel=current.get("channel", "?"),
                hidden_ssid=1 if current.get("ssid", "") == "" else 0,
            )
        )

    return records


def _parse_linux_nmcli(output: str) -> list[NetworkRecord]:
    records: list[NetworkRecord] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split(":")
        if len(parts) < 6:
            continue

        ssid, bssid, signal, channel, security, hidden = parts[:6]
        records.append(
            NetworkRecord(
                ssid=ssid or "<hidden>",
                bssid=bssid or "N/A",
                signal_strength=int(signal or 0),
                security_type=_normalize_security(security),
                channel=channel or "?",
                hidden_ssid=1 if hidden.lower() == "yes" else 0,
            )
        )
    return records


def _sample_records() -> list[NetworkRecord]:
    return [
        NetworkRecord("CampusGuest", "AA:11:22:33:44:01", 82, "OPEN", "11", 1, 0, 1),
        NetworkRecord("Lab-WPA2", "AA:11:22:33:44:02", 69, "WPA2", "1", 0, 0, 0),
        NetworkRecord("Office-IoT", "AA:11:22:33:44:03", 58, "WPA", "6", 1, 0, 1),
        NetworkRecord("<hidden>", "AA:11:22:33:44:04", 47, "WEP", "3", 0, 1, 1),
        NetworkRecord("SecureNet", "AA:11:22:33:44:05", 73, "WPA3", "36", 0, 0, 0),
    ]


def scan_networks(simulate: bool = False) -> list[NetworkRecord]:
    if simulate:
        return _sample_records()

    system = platform.system().lower()
    if "windows" in system:
        output = _safe_run(["netsh", "wlan", "show", "networks", "mode=bssid"])
        records = _parse_windows_netsh(output)
        return records if records else _sample_records()

    output = _safe_run(
        [
            "nmcli",
            "-t",
            "-f",
            "SSID,BSSID,SIGNAL,CHAN,SECURITY,HIDDEN",
            "device",
            "wifi",
            "list",
        ]
    )
    records = _parse_linux_nmcli(output)
    return records if records else _sample_records()


def to_frame(records: Iterable[NetworkRecord]):
    import pandas as pd

    return pd.DataFrame(
        [
            {
                "ssid": r.ssid,
                "bssid": r.bssid,
                "signal_strength": r.signal_strength,
                "security_type": r.security_type,
                "channel": r.channel,
                "wps_enabled": r.wps_enabled,
                "hidden_ssid": r.hidden_ssid,
                "known_vendor_risk": r.known_vendor_risk,
            }
            for r in records
        ]
    )
