#!/usr/bin/env python3
"""Telemetry Analyzer

A practical log-analysis utility that reviews operational output, extracts
suspicious patterns, and summarizes likely risk areas in a readable format.
This is intended for lab use and defensive review, not for active exploitation.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class LogEvent:
    timestamp: str
    source: str
    level: str
    message: str


@dataclass
class Alert:
    type: str
    severity: str
    message: str
    count: int = 1


@dataclass
class AnalysisReport:
    source_file: str
    total_events: int
    parse_errors: int
    warning_events: int
    info_events: int
    suspicious_patterns: list[Alert] = field(default_factory=list)
    generated_at: str = ""


SEVERITY_ORDER = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
SCAN_PATTERNS = [
    re.compile(r"scan|recon|port.*probe|connection.*burst", re.IGNORECASE),
    re.compile(r"failed.*login|authentication.*failure|bruteforce", re.IGNORECASE),
    re.compile(r"suspicious.*process|unexpected.*binary|shell.*spawn", re.IGNORECASE),
    re.compile(r"entropy.*high|malware.*signature|suspicious.*network", re.IGNORECASE),
]


def parse_log_line(raw: str) -> LogEvent | None:
    line = raw.strip()
    if not line:
        return None
    parts = line.split(" ", 4)
    if len(parts) < 4:
        return None
    timestamp, source, level, message = parts[0], parts[1], parts[2], parts[3]
    return LogEvent(timestamp=timestamp, source=source, level=level, message=message)


def summarize_logs(log_path: Path) -> AnalysisReport:
    total_events = 0
    parse_errors = 0
    warning_events = 0
    info_events = 0
    alerts: dict[str, Alert] = {}

    with log_path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            event = parse_log_line(raw_line)
            if event is None:
                parse_errors += 1
                continue

            total_events += 1
            if event.level.upper() == "WARNING":
                warning_events += 1
            if event.level.upper() == "INFO":
                info_events += 1

            matched = False
            for pattern in SCAN_PATTERNS:
                if pattern.search(event.message):
                    key = pattern.pattern
                    alert = alerts.setdefault(key, Alert(type="pattern", severity="MEDIUM", message=event.message, count=0))
                    alert.count += 1
                    if event.level.upper() in {"CRITICAL", "HIGH"}:
                        alert.severity = event.level.upper()
                    matched = True
                    break

            if not matched and any(keyword in event.message.lower() for keyword in ["suspicious", "failed", "scan", "recon", "burst"]):
                alert = alerts.setdefault("generic-suspicion", Alert(type="generic", severity="LOW", message="Possible suspicious activity", count=0))
                alert.count += 1

    return AnalysisReport(
        source_file=str(log_path),
        total_events=total_events,
        parse_errors=parse_errors,
        warning_events=warning_events,
        info_events=info_events,
        suspicious_patterns=list(alerts.values()),
        generated_at=datetime.utcnow().isoformat() + "Z",
    )


def print_report(report: AnalysisReport) -> None:
    print(f"Source: {report.source_file}")
    print(f"Total events: {report.total_events}")
    print(f"Parse errors: {report.parse_errors}")
    print(f"Warning events: {report.warning_events}")
    print(f"Info events: {report.info_events}")
    print("\nSuspicious patterns:")
    if not report.suspicious_patterns:
        print("  No suspicious patterns detected.")
        return

    for alert in sorted(report.suspicious_patterns, key=lambda item: (SEVERITY_ORDER.get(item.severity, 0), item.count), reverse=True):
        print(f"  - {alert.severity}: {alert.message} (count={alert.count})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Review operational telemetry for suspicious patterns.")
    parser.add_argument("--log", required=True, type=Path, help="Path to a telemetry log file")
    parser.add_argument("--json", action="store_true", help="Emit output as JSON")
    args = parser.parse_args()

    report = summarize_logs(args.log)
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
