#!/usr/bin/env python3
"""
Port & Service Scanner
-----------------------
A multithreaded TCP connect-scanner with banner grabbing.

Usage:
    python3 01_port_scanner.py 192.168.1.10 -p 1-1024
    python3 01_port_scanner.py scanme.example.com -p 22,80,443,8080

Only run this against hosts you own or have explicit written
permission to test.
"""

from __future__ import annotations

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class ScanResult:
    port: int
    state: str
    banner: str | None = None


def parse_ports(port_spec: str) -> list[int]:
    """Parse '22,80,443' or '1-1024' or a mix of both into a sorted list of ints."""
    ports: set[int] = set()
    for chunk in port_spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            start, end = chunk.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        elif chunk:
            ports.add(int(chunk))
    return sorted(p for p in ports if 0 < p <= 65535)


def grab_banner(sock: socket.socket) -> str | None:
    """Try to read a short banner from an already-connected socket."""
    try:
        sock.settimeout(1.0)
        data = sock.recv(256)
        return data.decode(errors="replace").strip() or None
    except (socket.timeout, OSError):
        return None


def scan_port(host: str, port: int, timeout: float) -> ScanResult:
    """Attempt a TCP connect to a single port; grab a banner if it opens."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            banner = grab_banner(sock)
            return ScanResult(port=port, state="open", banner=banner)
    except (ConnectionRefusedError, OSError):
        return ScanResult(port=port, state="closed")
    except socket.timeout:
        return ScanResult(port=port, state="filtered")


def scan_host(host: str, ports: list[int], timeout: float, max_workers: int) -> list[ScanResult]:
    """Scan every port in `ports` concurrently and return only open/filtered results."""
    results: list[ScanResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(scan_port, host, p, timeout): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            if result.state != "closed":
                results.append(result)
    return sorted(results, key=lambda r: r.port)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple TCP connect port scanner.")
    parser.add_argument("host", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024", help="Ports, e.g. '1-1024' or '22,80,443'")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Per-port timeout in seconds")
    parser.add_argument("-w", "--workers", type=int, default=200, help="Concurrent worker threads")
    args = parser.parse_args()

    try:
        resolved_ip = socket.gethostbyname(args.host)
    except socket.gaierror as exc:
        raise SystemExit(f"Could not resolve host '{args.host}': {exc}")

    ports = parse_ports(args.ports)
    print(f"Scanning {args.host} ({resolved_ip}) — {len(ports)} ports...")

    results = scan_host(resolved_ip, ports, args.timeout, args.workers)

    if not results:
        print("No open or filtered ports found.")
        return

    print(f"\n{'PORT':<8}{'STATE':<10}BANNER")
    for r in results:
        print(f"{r.port:<8}{r.state:<10}{r.banner or ''}")


if __name__ == "__main__":
    main()
