#!/usr/bin/env python3
"""
File Integrity Monitor (FIM)
-------------------------------
Hashes a set of watched files/directories, stores a baseline, and on
later runs reports anything added, removed, or modified.

Usage:
    python3 07_file_integrity_monitor.py baseline /etc/passwd /etc/ssh/sshd_config --out baseline.json
    python3 07_file_integrity_monitor.py check --baseline baseline.json
    python3 07_file_integrity_monitor.py watch --baseline baseline.json --interval 30
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


def hash_file(path: Path, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def collect_files(paths: list[str]) -> list[Path]:
    """Expand a mix of file and directory paths into a flat list of files."""
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(f for f in p.rglob("*") if f.is_file())
        elif p.is_file():
            files.append(p)
        else:
            print(f"Warning: path not found, skipping: {p}")
    return files


def build_baseline(paths: list[str]) -> dict[str, dict]:
    baseline: dict[str, dict] = {}
    for f in collect_files(paths):
        try:
            stat = f.stat()
            baseline[str(f.resolve())] = {
                "sha256": hash_file(f),
                "size": stat.st_size,
                "mode": oct(stat.st_mode),
            }
        except (PermissionError, OSError) as exc:
            print(f"Warning: could not read {f}: {exc}")
    return baseline


def cmd_baseline(args: argparse.Namespace) -> None:
    baseline = build_baseline(args.paths)
    args.out.write_text(json.dumps(baseline, indent=2))
    print(f"Baseline written: {len(baseline)} files -> {args.out}")


def diff_against_baseline(baseline: dict[str, dict]) -> list[str]:
    """Returns a list of human-readable change descriptions."""
    changes: list[str] = []

    for path_str, record in baseline.items():
        path = Path(path_str)
        if not path.exists():
            changes.append(f"DELETED     {path_str}")
            continue

        try:
            current_hash = hash_file(path)
            current_mode = oct(path.stat().st_mode)
        except (PermissionError, OSError) as exc:
            changes.append(f"UNREADABLE  {path_str} ({exc})")
            continue

        if current_hash != record["sha256"]:
            changes.append(f"MODIFIED    {path_str}")
        elif current_mode != record["mode"]:
            changes.append(f"PERMS CHANGED {path_str} ({record['mode']} -> {current_mode})")

    return changes


def cmd_check(args: argparse.Namespace) -> None:
    baseline = json.loads(args.baseline.read_text())
    changes = diff_against_baseline(baseline)

    if not changes:
        print("OK — no changes detected.")
    else:
        print(f"{len(changes)} change(s) detected:")
        for line in changes:
            print(f"  {line}")


def cmd_watch(args: argparse.Namespace) -> None:
    baseline = json.loads(args.baseline.read_text())
    print(f"Watching {len(baseline)} files every {args.interval}s (Ctrl+C to stop)...")
    try:
        while True:
            changes = diff_against_baseline(baseline)
            if changes:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {len(changes)} change(s) detected:")
                for line in changes:
                    print(f"  {line}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


def main() -> None:
    parser = argparse.ArgumentParser(description="File integrity monitor.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_baseline = sub.add_parser("baseline", help="Create a new baseline")
    p_baseline.add_argument("paths", nargs="+", help="Files or directories to baseline")
    p_baseline.add_argument("--out", type=Path, required=True, help="Output JSON baseline file")
    p_baseline.set_defaults(func=cmd_baseline)

    p_check = sub.add_parser("check", help="Compare current state to a baseline once")
    p_check.add_argument("--baseline", type=Path, required=True)
    p_check.set_defaults(func=cmd_check)

    p_watch = sub.add_parser("watch", help="Continuously re-check on an interval")
    p_watch.add_argument("--baseline", type=Path, required=True)
    p_watch.add_argument("--interval", type=float, default=30.0, help="Seconds between checks")
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
