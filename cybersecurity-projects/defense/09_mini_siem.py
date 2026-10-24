#!/usr/bin/env python3
"""
Mini SIEM / Log Correlation Engine
--------------------------------------
Ingests normalized security events into SQLite and runs a simple
cross-host correlation rule: the same source IP failing login on
multiple distinct hosts within a short window (lateral-movement /
credential-stuffing signature).

Feed it events from your own tools (e.g. 04_hids.py, 07_file_integrity_monitor.py)
or test it with the --demo flag to generate synthetic events.

Usage:
    python3 09_mini_siem.py init --db siem.db
    python3 09_mini_siem.py ingest --db siem.db --host web1 --type failed_login --src-ip 10.0.0.5 --detail "user=admin"
    python3 09_mini_siem.py correlate --db siem.db --min-hosts 3 --window 300
    python3 09_mini_siem.py demo --db siem.db
"""

from __future__ import annotations

import argparse
import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    host TEXT NOT NULL,
    event_type TEXT NOT NULL,
    src_ip TEXT,
    detail TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_src_ip ON events(src_ip);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
"""


def get_connection(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def cmd_init(args: argparse.Namespace) -> None:
    conn = get_connection(args.db)
    conn.executescript(SCHEMA)
    conn.commit()
    print(f"Initialized database at {args.db}")


def cmd_ingest(args: argparse.Namespace) -> None:
    conn = get_connection(args.db)
    conn.execute(
        "INSERT INTO events (timestamp, host, event_type, src_ip, detail) VALUES (?, ?, ?, ?, ?)",
        (time.time(), args.host, args.type, args.src_ip, args.detail),
    )
    conn.commit()
    print(f"Ingested event: host={args.host} type={args.type} src_ip={args.src_ip}")


def cmd_demo(args: argparse.Namespace) -> None:
    """Insert a synthetic attack pattern so you can see correlate() catch something."""
    conn = get_connection(args.db)
    conn.executescript(SCHEMA)
    now = time.time()
    attacker_ip = "203.0.113.42"
    hosts = ["web1", "web2", "db1", "app1"]

    rows = [
        (now + i * 2, host, "failed_login", attacker_ip, "user=admin")
        for i, host in enumerate(hosts)
    ]
    rows.append((now + 20, "db1", "login_success", attacker_ip, "user=admin"))

    conn.executemany(
        "INSERT INTO events (timestamp, host, event_type, src_ip, detail) VALUES (?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()
    print(f"Inserted {len(rows)} synthetic demo events for src_ip={attacker_ip}")


def correlate_multi_host_failures(conn: sqlite3.Connection, min_hosts: int, window_seconds: float) -> list[dict]:
    """
    Rule: same src_ip has 'failed_login' events on >= min_hosts distinct
    hosts, all within window_seconds of each other.
    """
    cursor = conn.execute(
        "SELECT src_ip, host, timestamp FROM events "
        "WHERE event_type = 'failed_login' AND src_ip IS NOT NULL "
        "ORDER BY src_ip, timestamp"
    )
    rows = cursor.fetchall()

    by_ip: dict[str, list[tuple[float, str]]] = {}
    for row in rows:
        by_ip.setdefault(row["src_ip"], []).append((row["timestamp"], row["host"]))

    alerts = []
    for ip, events in by_ip.items():
        events.sort()
        window_start = 0
        for i in range(len(events)):
            while events[i][0] - events[window_start][0] > window_seconds:
                window_start += 1
            hosts_in_window = {h for _, h in events[window_start : i + 1]}
            if len(hosts_in_window) >= min_hosts:
                alerts.append({
                    "src_ip": ip,
                    "distinct_hosts": sorted(hosts_in_window),
                    "window_seconds": window_seconds,
                })
                break
    return alerts


def check_success_after_failures(conn: sqlite3.Connection, window_seconds: float) -> list[dict]:
    """Rule: a login_success shortly after that same src_ip had failed_login events elsewhere."""
    cursor = conn.execute(
        "SELECT src_ip, host, timestamp, event_type FROM events "
        "WHERE event_type IN ('failed_login', 'login_success') AND src_ip IS NOT NULL "
        "ORDER BY src_ip, timestamp"
    )
    rows = cursor.fetchall()

    by_ip: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        by_ip.setdefault(row["src_ip"], []).append(row)

    alerts = []
    for ip, events in by_ip.items():
        failures = [e for e in events if e["event_type"] == "failed_login"]
        successes = [e for e in events if e["event_type"] == "login_success"]
        for success in successes:
            recent_failures = [
                f for f in failures
                if 0 <= success["timestamp"] - f["timestamp"] <= window_seconds
            ]
            if recent_failures:
                alerts.append({
                    "src_ip": ip,
                    "success_host": success["host"],
                    "prior_failed_hosts": sorted({f["host"] for f in recent_failures}),
                })
    return alerts


def cmd_correlate(args: argparse.Namespace) -> None:
    conn = get_connection(args.db)

    scan_alerts = correlate_multi_host_failures(conn, args.min_hosts, args.window)
    success_alerts = check_success_after_failures(conn, args.window)

    if scan_alerts:
        print(f"\n[RULE] Multi-host failed logins (possible credential stuffing):")
        for alert in scan_alerts:
            print(f"  src_ip={alert['src_ip']} hit {len(alert['distinct_hosts'])} hosts "
                  f"within {alert['window_seconds']:.0f}s: {alert['distinct_hosts']}")

    if success_alerts:
        print(f"\n[RULE] Success following failures (possible successful brute-force):")
        for alert in success_alerts:
            print(f"  src_ip={alert['src_ip']} succeeded on {alert['success_host']} "
                  f"after failing on {alert['prior_failed_hosts']}")

    if not scan_alerts and not success_alerts:
        print("No correlated alerts found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mini SIEM log correlation engine.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create a new SQLite event store")
    p_init.add_argument("--db", type=Path, required=True)
    p_init.set_defaults(func=cmd_init)

    p_ingest = sub.add_parser("ingest", help="Insert one event")
    p_ingest.add_argument("--db", type=Path, required=True)
    p_ingest.add_argument("--host", required=True)
    p_ingest.add_argument("--type", required=True, help="e.g. failed_login, login_success, fim_alert")
    p_ingest.add_argument("--src-ip")
    p_ingest.add_argument("--detail", default="")
    p_ingest.set_defaults(func=cmd_ingest)

    p_demo = sub.add_parser("demo", help="Insert synthetic events to test correlation")
    p_demo.add_argument("--db", type=Path, required=True)
    p_demo.set_defaults(func=cmd_demo)

    p_correlate = sub.add_parser("correlate", help="Run correlation rules over stored events")
    p_correlate.add_argument("--db", type=Path, required=True)
    p_correlate.add_argument("--min-hosts", type=int, default=3)
    p_correlate.add_argument("--window", type=float, default=300.0, help="Seconds")
    p_correlate.set_defaults(func=cmd_correlate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
