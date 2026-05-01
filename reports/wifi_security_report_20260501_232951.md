# WiFi Security Assessment Report

Generated: 2026-05-01 23:29:51

## Scope
- Defensive assessment only
- For authorized networks/labs

## Network Risk Findings
- High risk networks: 3
- Medium risk networks: 0
- Low risk networks: 2

Top 5 by risk score:

| ssid        | security_type | signal_strength | risk_score | risk_label |
| ----------- | ------------- | --------------- | ---------- | ---------- |
| CampusGuest | OPEN          | 82              | 100.0      | High       |
| Office-IoT  | WPA           | 58              | 100.0      | High       |
| <hidden>    | WEP           | 47              | 100.0      | High       |
| SecureNet   | WPA3          | 73              | 0.0        | Low        |
| Lab-WPA2    | WPA2          | 69              | 0.0        | Low        |

## Password Policy Check
- Score: 95/100
- Rating: Strong
- Findings:
  - No major weaknesses detected.
- Recommendations:
  - Password is strong. Rotate periodically and avoid re-use.

## Traffic Anomaly Summary
No traffic dataset analyzed.

## Real-Time Alerts
- [CRITICAL] Detected 1 open network(s). Enforce WPA2/WPA3 immediately.
- [CRITICAL] Detected 1 WEP network(s). Migrate to WPA3 or WPA2-AES.
- [HIGH] 3 high-risk network(s) need urgent hardening.

## Adaptive Learning Insights
- No adverse trend detected in recent assessments.

## Recommended Hardening
- Prefer WPA3 or WPA2-AES; disable WEP/WPA and open networks.
- Disable WPS on production access points.
- Enforce long unique passphrases with periodic rotation.
- Monitor abnormal traffic bursts and unusual protocol mixes.