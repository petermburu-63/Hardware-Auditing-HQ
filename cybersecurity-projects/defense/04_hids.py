#!/usr/bin/env python3
"""
Host-Based Intrusion Detection System (HIDS) - core module
--------------------------------------------------------------
Tails an auth/log file and alerts on a threshold-based rule:
N failed login attempts from the same source IP within a time window.

Designed for Linux-style "Failed password ... from <ip>" log lines
(e.g. /var/log/auth.log), but the regex is easy to adapt to other
formats.

Usage:
    python3 04_hids.py --logfile /var/log/auth.log --threshold 5 --window 60
"""

from __future__ import annotations

import argparse
import re
import time
from collections import defaultdict, deque
from pathlib import Path

FAILED_LOGIN_RE = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>[\d.]+)"
)


class BruteForceDetector:
    """Sliding-window counter of failed logins per source IP."""

    def __init__(self, threshold: int, window_seconds: float) -> None:
        self.threshold = threshold
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._alerted: set[str] = set()

    def record_failure(self, ip: str) -> bool:
        now = time.time()
        events = self._events[ip]
        events.append(now)

        while events and now - events[0] > self.window_seconds:
            events.popleft()

        if len(events) >= self.threshold:
            if ip not in self._alerted:
                self._alerted.add(ip)
                return True
        else:
            self._alerted.discard(ip)
        return False


def tail_file(path: Path):
    """Generator that yields new lines appended to `path`, like `tail -f`."""
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple threshold-based brute-force log watcher.")
    parser.add_argument("--logfile", type=Path, required=True, help="Path to an auth log file to tail")
    parser.add_argument("--threshold", type=int, default=5, help="Failed attempts to trigger an alert")
    parser.add_argument("--window", type=float, default=60.0, help="Sliding window in seconds")
    args = parser.parse_args()

    if not args.logfile.exists():
        raise SystemExit(f"Log file not found: {args.logfile}")

    detector = BruteForceDetector(threshold=args.threshold, window_seconds=args.window)

    print(f"Watching {args.logfile} for brute-force patterns "
          f"(>= {args.threshold} fails / {args.window:.0f}s)...")

    for line in tail_file(args.logfile):
        match = FAILED_LOGIN_RE.search(line)
        if not match:
            continue

        ip = match.group("ip")
        user = match.group("user")

        if detector.record_failure(ip):
            print(f"[ALERT] Brute-force suspected from {ip} "
                  f"(>= {args.threshold} failed logins in {args.window:.0f}s, "
                  f"most recent target user: '{user}')")


if __name__ == "__main__":
    main()
