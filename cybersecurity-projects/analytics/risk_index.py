#!/usr/bin/env python3
"""Host Guard

A defensive monitoring utility that tracks file integrity, records baseline state,
and flags suspicious drift. It is designed for a lab or controlled security review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from time import sleep, time

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None


@dataclass
class GuardRecord:
    path: str
    sha256: str
    size: int
    modified: float


@dataclass
class GuardSnapshot:
    scanned_at: float
    base_dir: str
    files: dict[str, GuardRecord] = field(default_factory=dict)
    system_summary: dict[str, float] = field(default_factory=dict)


def sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_snapshot(root: Path) -> GuardSnapshot:
    records: dict[str, GuardRecord] = {}
    for item in sorted(root.rglob("*")):
        if item.is_file():
            stat = item.stat()
            records[item.relative_to(root).as_posix()] = GuardRecord(
                path=item.relative_to(root).as_posix(),
                sha256=sha256_of_file(item),
                size=stat.st_size,
                modified=stat.st_mtime,
            )

    summary: dict[str, float] = {}
    if psutil is not None:
        process = psutil.Process()
        with process.oneshot():
            summary["cpu_percent"] = process.cpu_percent(interval=None)
            summary["memory_percent"] = process.memory_percent()

    return GuardSnapshot(scanned_at=time(), base_dir=str(root), files=records, system_summary=summary)


def detect_drift(before: GuardSnapshot, after: GuardSnapshot) -> list[str]:
    drift: list[str] = []
    for rel_path, current in after.files.items():
        previous = before.files.get(rel_path)
        if previous is None:
            drift.append(f"NEW FILE: {rel_path}")
        elif previous.sha256 != current.sha256 or previous.size != current.size:
            drift.append(f"MODIFIED: {rel_path}")

    for rel_path in before.files:
        if rel_path not in after.files:
            drift.append(f"REMOVED: {rel_path}")

    if after.system_summary != before.system_summary:
        drift.append("SYSTEM SUMMARY CHANGED")

    return drift


def run_guard(path: Path, interval: float, iterations: int) -> None:
    baseline = collect_snapshot(path)
    for idx in range(iterations):
        sleep(interval)
        current = collect_snapshot(path)
        drift = detect_drift(baseline, current)
        if drift:
            print(f"[{idx + 1}] Drift detected:")
            for item in drift:
                print(f"  - {item}")
        else:
            print(f"[{idx + 1}] No drift detected.")
        baseline = current


def main() -> None:
    parser = argparse.ArgumentParser(description="Baseline and monitor a directory for drift and file integrity issues.")
    parser.add_argument("--path", required=True, type=Path, help="Directory to monitor")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds")
    parser.add_argument("--iterations", type=int, default=3, help="Monitoring cycles")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"Path does not exist: {args.path}")

    baseline = collect_snapshot(args.path)
    if args.json:
        print(json.dumps({"baseline": {k: v.__dict__ for k, v in baseline.files.items()}, "system_summary": baseline.system_summary}, indent=2))
        return

    run_guard(args.path, args.interval, args.iterations)


if __name__ == "__main__":
    main()
