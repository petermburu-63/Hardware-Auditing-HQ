#!/usr/bin/env python3
"""Advanced Reconnaissance Suite

A lab-safe network reconnaissance utility that demonstrates how structured
service discovery tools collect host metadata, test TCP ports, and summarize
open services without performing unauthorized exploitation.

This script is intentionally limited to observation, reporting, and baseline
collection for educational use.
"""

from __future__ import annotations

import argparse
import json
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Iterable


@dataclass
class PortResult:
    port: int
    state: str
    service: str = "unknown"
    banner: str | None = None
    latency_ms: float = 0.0


@dataclass
class HostSummary:
    host: str
    resolved_ip: str
    scanned_ports: list[int] = field(default_factory=list)
    open_ports: list[PortResult] = field(default_factory=list)
    timestamp: str = ""


SERVICE_HINTS = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    465: "smtps",
    3306: "mysql",
    5432: "postgresql",
    8080: "http-alt",
    8443: "https-alt",
}


def resolve_hostname(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        raise SystemExit(f"Could not resolve host '{host}': {exc}") from exc


def parse_port_range(raw: str) -> list[int]:
    ports: set[int] = set()
    for part in raw.split(","):
        cleaned = part.strip()
        if not cleaned:
            continue
        if "-" in cleaned:
            start_text, end_text = cleaned.split("-", 1)
            try:
                start = int(start_text)
                end = int(end_text)
            except ValueError as exc:
                raise SystemExit(f"Invalid port range: '{cleaned}'") from exc
            ports.update(range(max(1, min(start, end)), min(65535, max(start, end)) + 1))
        else:
            try:
                value = int(cleaned)
            except ValueError as exc:
                raise SystemExit(f"Invalid port value: '{cleaned}'") from exc
            ports.add(max(1, min(value, 65535)))
    return sorted(ports)


def banner_grab(host: str, port: int, timeout: float = 0.8) -> tuple[str | None, float]:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            if port in (80, 8080, 8000):
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            data = sock.recv(512)
            banner = data.decode(errors="replace").strip() or None
            return banner, (time.perf_counter() - start) * 1000
    except (socket.timeout, OSError):
        return None, (time.perf_counter() - start) * 1000


def normalize_banner(banner: str | None, port: int) -> tuple[str, str | None]:
    if banner is None:
        return SERVICE_HINTS.get(port, "unknown"), None

    text = banner.replace("\r", " ").replace("\n", " ").strip()
    if len(text) > 180:
        text = text[:177] + "..."

    inferred = SERVICE_HINTS.get(port, "unknown")
    for token in ("SSH", "HTTP", "Apache", "nginx", "POSTGRESQL", "MYSQL", "SMTP", "IMAP", "POP3", "FTP"):
        if token.lower() in text.lower():
            inferred = token.lower()
            break

    return inferred, text


def scan_port(host: str, port: int, timeout: float = 0.8) -> PortResult:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            banner, _ = banner_grab(host, port, timeout)
            service, clean_banner = normalize_banner(banner, port)
            latency_ms = (time.perf_counter() - start) * 1000
            return PortResult(
                port=port,
                state="open",
                service=service,
                banner=clean_banner,
                latency_ms=round(latency_ms, 2),
            )
    except (socket.error, OSError):
        latency_ms = (time.perf_counter() - start) * 1000
        return PortResult(
            port=port,
            state="closed",
            service=SERVICE_HINTS.get(port, "unknown"),
            latency_ms=round(latency_ms, 2),
        )


def scan_target(host: str, ports: Iterable[int], timeout: float = 0.7, workers: int = 50) -> list[PortResult]:
    results: list[PortResult] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(scan_port, host, port, timeout): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result.state == "open":
                results.append(result)
    return sorted(results, key=lambda item: item.port)


def build_summary(host: str, ports: list[int], scan_results: list[PortResult]) -> HostSummary:
    return HostSummary(
        host=host,
        resolved_ip=resolve_hostname(host),
        scanned_ports=ports,
        open_ports=scan_results,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def print_summary(summary: HostSummary) -> None:
    print(f"\nHost: {summary.host}")
    print(f"Resolved IP: {summary.resolved_ip}")
    print(f"Scan time: {summary.timestamp}")
    print(f"Scanned ports: {len(summary.scanned_ports)}")
    print(f"Open ports: {len(summary.open_ports)}")

    if not summary.open_ports:
        print("No open ports detected.")
        return

    print("\nPORT  STATE  SERVICE       LATENCY(ms)  BANNER")
    for item in summary.open_ports:
        banner = item.banner or "-"
        print(f"{item.port:<5} {item.state:<5} {item.service:<12} {item.latency_ms:<11.2f} {banner}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Educational reconnaissance and service discovery utility.")
    parser.add_argument("--host", required=True, help="Target IP or hostname to examine")
    parser.add_argument("--ports", default="1-1024", help="Example: '22,80,443' or '1-1024'")
    parser.add_argument("--timeout", type=float, default=0.8, help="Socket timeout in seconds")
    parser.add_argument("--workers", type=int, default=50, help="Thread worker count for scans")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of terminal output")
    args = parser.parse_args()

    ports = parse_port_range(args.ports)
    results = scan_target(args.host, ports, timeout=args.timeout, workers=args.workers)
    summary = build_summary(args.host, ports, results)

    if args.json:
        print(json.dumps({"host": summary.host, "resolved_ip": summary.resolved_ip, "timestamp": summary.timestamp, "open_ports": [asdict(item) for item in summary.open_ports]}, indent=2))
        return

    print_summary(summary)


if __name__ == "__main__":
    main()
