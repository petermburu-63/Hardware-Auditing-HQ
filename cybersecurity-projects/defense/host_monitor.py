#!/usr/bin/env python3
"""Host Monitor

A defensive monitoring utility that snapshots a target directory, records file
hashes, and reports any changes between inspection cycles.
This is designed for lab environments and educational integrity monitoring.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from time import sleep, time


@dataclass
class FileState:
    path: str
    sha256: str
    size: int
    modified: float


@dataclass
class MonitorSnapshot:
    scanned_at: float
    base_dir: str
    files: dict[str, FileState] = field(default_factory=dict)
    changes: list[str] = field(default_factory=list)


def sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_snapshot(root: Path) -> MonitorSnapshot:
    files: dict[str, FileState] = {}
    for item in sorted(root.rglob("*")):
        if item.is_file():
            stat = item.stat()
            files[item.relative_to(root).as_posix()] = FileState(
                path=item.relative_to(root).as_posix(),
                sha256=sha256_of_file(item),
                size=stat.st_size,
                modified=stat.st_mtime,
            )
    return MonitorSnapshot(scanned_at=time(), base_dir=str(root), files=files, changes=[])


def detect_changes(before: MonitorSnapshot, after: MonitorSnapshot) -> list[str]:
    changes: list[str] = []
    before_lookup = before.files
    after_lookup = after.files

    for rel_path, current in after_lookup.items():
        previous = before_lookup.get(rel_path)
        if previous is None:
            changes.append(f"NEW FILE: {rel_path}")
        elif previous.sha256 != current.sha256 or previous.size != current.size:
            changes.append(f"MODIFIED: {rel_path}")

    for rel_path in before_lookup:
        if rel_path not in after_lookup:
            changes.append(f"REMOVED: {rel_path}")

    return changes


def run_monitor(path: Path, interval: float, iterations: int) -> None:
    baseline = collect_snapshot(path)
    for idx in range(iterations):
        sleep(interval)
        snapshot = collect_snapshot(path)
        changes = detect_changes(baseline, snapshot)
        if changes:
            print(f"[{idx + 1}] Change detected:")
            for change in changes:
                print(f"  - {change}")
        else:
            print(f"[{idx + 1}] No changes detected.")
        baseline = snapshot


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor a directory for file integrity changes.")
    parser.add_argument("--path", required=True, type=Path, help="Target directory to monitor")
    parser.add_argument("--interval", type=float, default=5.0, help="Polling interval in seconds")
    parser.add_argument("--iterations", type=int, default=3, help="Number of cycles")
    parser.add_argument("--json", action="store_true", help="Emit a JSON snapshot")
    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"Path does not exist: {args.path}")

    baseline = collect_snapshot(args.path)
    if args.json:
        print(json.dumps({"baseline": {k: v.__dict__ for k, v in baseline.files.items()}}, indent=2))
        return

    run_monitor(args.path, args.interval, args.iterations)


if __name__ == "__main__":
    main()
