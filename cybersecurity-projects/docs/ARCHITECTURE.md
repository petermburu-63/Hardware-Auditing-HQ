#!/usr/bin/env python3
"""Risk Index Analyzer

Evaluates a JSON event stream and produces a weighted risk score based on the
volume and severity of suspicious patterns. This is a simple analytical model for
lab-based telemetry review.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path


SEVERITY_WEIGHTS = {
    "LOW": 1,
    "MEDIUM": 3,
    "HIGH": 6,
    "CRITICAL": 10,
}


@dataclass
class RiskObservation:
    source: str
    severity: str
    label: str
    count: int = 1


@dataclass
class RiskSummary:
    total_events: int
    total_risk_score: int
    observations: list[RiskObservation] = field(default_factory=list)


def score_events(entries: list[dict]) -> RiskSummary:
    observations: list[RiskObservation] = []
    score = 0

    for item in entries:
        label = str(item.get("label", "unknown"))
        severity = str(item.get("severity", "LOW")).upper()
        source = str(item.get("source", "anonymous"))
        count = int(item.get("count", 1))

        score += SEVERITY_WEIGHTS.get(severity, 1) * count
        observations.append(RiskObservation(source=source, severity=severity, label=label, count=count))

    return RiskSummary(total_events=len(entries), total_risk_score=score, observations=observations)


def print_summary(summary: RiskSummary) -> None:
    print(f"Total events: {summary.total_events}")
    print(f"Total risk score: {summary.total_risk_score}")
    if not summary.observations:
        print("No observations to score.")
        return

    print("\nObservation breakdown:")
    for obs in summary.observations:
        print(f"- {obs.source}: {obs.label} [{obs.severity}] x{obs.count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score event data to produce a simple operational risk summary.")
    parser.add_argument("--events", required=True, type=Path, help="Path to a JSON event list")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    with args.events.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    results = score_events(payload if isinstance(payload, list) else [payload])

    if args.json:
        print(json.dumps({
            "total_events": results.total_events,
            "total_risk_score": results.total_risk_score,
            "observations": [{"source": x.source, "severity": x.severity, "label": x.label, "count": x.count} for x in results.observations],
        }, indent=2))
        return

    print_summary(results)


if __name__ == "__main__":
    main()
