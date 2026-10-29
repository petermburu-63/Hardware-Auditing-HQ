#!/usr/bin/env python3
"""Host Discovery Engine

A stronger discovery utility for structured host review. It resolves a target,
checks a port range, and summarizes open services with simple classifications.

This script is lab-safe and designed for controlled environments only.
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
class EndpointResult:
    port: int
    state: str
    service: str = "unknown"
    banner: str | None = None
    latency_ms: float = 0.0


@dataclass
class HostDiscoveryReport:
    host: str
    resolved_ip: str
    timestamp: str
    ports_scanned: list[int] = field(default_factory=list)
    open_ports: list[EndpointResult] = field(default_factory=list)


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


def parse_ports(raw: str) -> list[int]:
    ports: set[int] = set()
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_text, end_text = chunk.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            ports.update(range(max(1, min(start, end)), min(65535, max(start, end)) + 1))
        else:
            ports.add(max(1, min(int(chunk), 65535)))
    return sorted(ports)


def resolve_hostname(host: str) -> str:
    try:
        return socket.gethostbyname(host)
    except socket.gaierror as exc:
        raise SystemExit(f"Could not resolve host '{host}': {exc}") from exc


def banner_grab(host: str, port: int, timeout: float = 0.6) -> tuple[str | None, float]:
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


def normalize_service(port: int, banner: str | None) -> tuple[str, str | None]:
    if banner is None:
        return SERVICE_HINTS.get(port, "unknown"), None

    text = banner.replace("\r", " ").replace("\n", " ").strip()
    if len(text) > 200:
        text = text[:197] + "..."

    inferred = SERVICE_HINTS.get(port, "unknown")
    for keyword in ("SSH", "HTTP", "Apache", "nginx", "MySQL", "POSTGRESQL", "SMTP", "IMAP", "POP3", "FTP"):
        if keyword.lower() in text.lower():
            inferred = keyword.lower()
            break
    return inferred, text


def scan_port(host: str, port: int, timeout: float) -> EndpointResult:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            banner, _ = banner_grab(host, port, timeout)
            service, clean_banner = normalize_service(port, banner)
            latency_ms = (time.perf_counter() - start) * 1000
            return EndpointResult(port=port, state="open", service=service, banner=clean_banner, latency_ms=round(latency_ms, 2))
    except (socket.timeout, OSError):
        latency_ms = (time.perf_counter() - start) * 1000
        return EndpointResult(port=port, state="closed", service=SERVICE_HINTS.get(port, "unknown"), latency_ms=round(latency_ms, 2))


def scan_host(host: str, ports: Iterable[int], timeout: float, workers: int = 50) -> list[EndpointResult]:
    results: list[EndpointResult] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(scan_port, host, port, timeout): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result.state == "open":
                results.append(result)
    return sorted(results, key=lambda item: item.port)


def build_report(host: str, ports: list[int], discovered: list[EndpointResult]) -> HostDiscoveryReport:
    return HostDiscoveryReport(
        host=host,
        resolved_ip=resolve_hostname(host),
        timestamp=datetime.now(timezone.utc).isoformat(),
        ports_scanned=ports,
        open_ports=discovered,
    )


def print_report(report: HostDiscoveryReport) -> None:
    print(f"Host: {report.host}")
    print(f"Resolved IP: {report.resolved_ip}")
    print(f"Timestamp: {report.timestamp}")
    print(f"Ports scanned: {len(report.ports_scanned)}")
    print(f"Open endpoints: {len(report.open_ports)}")

    if not report.open_ports:
        print("No open endpoints detected.")
        return

    print("\nPORT  SERVICE        LATENCY(ms)  BANNER")
    for item in report.open_ports:
        print(f"{item.port:<5} {item.service:<14} {item.latency_ms:<11.2f} {item.banner or '-'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Structured host discovery and service review utility.")
    parser.add_argument("--host", required=True, help="Target hostname or IP")
    parser.add_argument("--ports", default="1-1024", help="Port range or list, e.g. '22,80,443' or '1-1024'")
    parser.add_argument("--timeout", type=float, default=0.7, help="Socket timeout in seconds")
    parser.add_argument("--workers", type=int, default=50, help="Worker pool size")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    ports = parse_ports(args.ports)
    results = scan_host(args.host, ports, args.timeout, args.workers)
    report = build_report(args.host, ports, results)

    if args.json:
        print(json.dumps({"host": report.host, "resolved_ip": report.resolved_ip, "timestamp": report.timestamp, "open_ports": [asdict(item) for item in report.open_ports]}, indent=2))
        return

    print_report(report)


if __name__ == "__main__":
    main()
