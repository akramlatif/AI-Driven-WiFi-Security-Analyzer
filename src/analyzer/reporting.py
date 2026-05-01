from datetime import datetime
from pathlib import Path

from .models import AutomationResult
from .protocols import ReportGenerator


def _dataframe_to_markdown(table) -> str:
    """
    Convert a small pandas DataFrame to a Markdown table without optional extras.
    """
    columns = [str(column) for column in table.columns]
    rows = [["" if value is None else str(value) for value in row] for row in table.itertuples(index=False, name=None)]

    widths = [len(column) for column in columns]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def format_row(values):
        cells = [value.ljust(widths[index]) for index, value in enumerate(values)]
        return f"| {' | '.join(cells)} |"

    header = format_row(columns)
    separator = f"| {' | '.join('-' * width for width in widths)} |"
    body = [format_row(row) for row in rows]
    return "\n".join([header, separator, *body])


class MarkdownReportGenerator(ReportGenerator):
    """
    Generates a WiFi security assessment report in Markdown format.
    """

    def build(self, result: AutomationResult) -> str:
        """
        Builds the Markdown report from an AutomationResult.

        Args:
            result: The structured result from an automated assessment run.

        Returns:
            A string containing the full Markdown report.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "# WiFi Security Assessment Report",
            "",
            f"Generated: {ts}",
            "",
            "## Scope",
            "- Defensive assessment only",
            "- For authorized networks/labs",
            "",
            "## Network Risk Findings",
        ]

        if result.network_table is None or result.network_table.empty:
            lines.extend(["No network scan data available.", ""])
        else:
            high = int((result.network_table["risk_label"] == "High").sum())
            med = int((result.network_table["risk_label"] == "Medium").sum())
            low = int((result.network_table["risk_label"] == "Low").sum())
            lines.extend(
                [
                    f"- High risk networks: {high}",
                    f"- Medium risk networks: {med}",
                    f"- Low risk networks: {low}",
                    "",
                    "Top 5 by risk score:",
                    "",
                ]
            )
            top = result.network_table[
                ["ssid", "security_type", "signal_strength", "risk_score", "risk_label"]
            ].head(5)
            lines.append(_dataframe_to_markdown(top))
            lines.append("")

        lines.append("## Password Policy Check")
        if result.password_result:
            lines.extend(
                [
                    f"- Score: {result.password_result.score}/100",
                    f"- Rating: {result.password_result.rating}",
                    "- Findings:",
                ]
            )
            lines.extend(
                [f"  - {item}" for item in result.password_result.findings]
                or ["  - No major weaknesses detected."]
            )
            lines.append("- Recommendations:")
            lines.extend([f"  - {item}" for item in result.password_result.recommendations])
        else:
            lines.append("No password sample audited.")
        lines.append("")

        lines.append("## Traffic Anomaly Summary")
        if result.traffic_result:
            lines.extend(
                [
                    f"- Anomaly rows: {result.traffic_result.anomaly_rows}/{result.traffic_result.total_rows}",
                    f"- Anomaly ratio: {result.traffic_result.anomaly_ratio:.4f}",
                    f"- Risk status: {result.traffic_result.status}",
                ]
            )
        else:
            lines.append("No traffic dataset analyzed.")
        lines.append("")

        lines.append("## Real-Time Alerts")
        if result.alerts:
            for alert in result.alerts:
                severity = str(alert.get("severity", "info")).upper()
                message = str(alert.get("message", ""))
                lines.append(f"- [{severity}] {message}")
        else:
            lines.append("No real-time alerts generated.")
        lines.append("")

        lines.append("## Adaptive Learning Insights")
        if result.adaptive_insights:
            lines.extend([f"- {item}" for item in result.adaptive_insights])
        else:
            lines.append("No adaptive learning insights available yet.")
        lines.append("")

        lines.extend(
            [
                "## Recommended Hardening",
                "- Prefer WPA3 or WPA2-AES; disable WEP/WPA and open networks.",
                "- Disable WPS on production access points.",
                "- Enforce long unique passphrases with periodic rotation.",
                "- Monitor abnormal traffic bursts and unusual protocol mixes.",
            ]
        )

        return "\n".join(lines)

    def write(self, report_text: str, output_dir: str = "reports") -> Path:
        """
        Writes the report text to a timestamped Markdown file.

        Args:
            report_text: The string content of the report.
            output_dir: The directory to save the report in.

        Returns:
            The path to the newly created report file.
        """
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        file_name = f"wifi_security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        target = path / file_name
        target.write_text(report_text, encoding="utf-8")
        return target


def build_markdown_report(result: AutomationResult) -> str:
    """
    Backwards-compatible helper that builds a markdown report.
    """
    return MarkdownReportGenerator().build(result)


def write_report(report_text: str, output_dir: str = "reports") -> Path:
    """
    Backwards-compatible helper that writes a markdown report to disk.
    """
    return MarkdownReportGenerator().write(report_text, output_dir=output_dir)

