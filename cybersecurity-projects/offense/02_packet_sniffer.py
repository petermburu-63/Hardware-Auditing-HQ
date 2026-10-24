#!/usr/bin/env python3
"""
Packet Sniffer & Traffic Analyzer
----------------------------------
Captures live traffic on an interface you own/administer and flags a
simple pattern: many distinct destination ports contacted by the same
source IP in a short window (a classic port-scan signature).

Requires: scapy   (pip install scapy)
Requires root/administrator privileges to open a raw socket.

Usage:
    sudo python3 02_packet_sniffer.py -i eth0
    sudo python3 02_packet_sniffer.py -i eth0 --threshold 15 --window 5
"""

from __future__ import annotations

import argparse
import time
from collections import defaultdict, deque

try:
    from scapy.all import sniff, IP, TCP  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("This script requires scapy: pip install scapy") from exc


class ScanDetector:
    """Tracks (src_ip -> recent distinct dst_ports) and flags scan-like bursts."""

    def __init__(self, threshold: int, window_seconds: float) -> None:
        self.threshold = threshold
        self.window_seconds = window_seconds
        self._events: dict[str, deque[tuple[float, int]]] = defaultdict(deque)
        self._already_alerted: set[str] = set()

    def record(self, src_ip: str, dst_port: int) -> bool:
        """Record one event; return True if this src_ip just crossed the threshold."""
        now = time.time()
        events = self._events[src_ip]
        events.append((now, dst_port))

        while events and now - events[0][0] > self.window_seconds:
            events.popleft()

        distinct_ports = {port for _, port in events}
        if len(distinct_ports) >= self.threshold:
            if src_ip not in self._already_alerted:
                self._already_alerted.add(src_ip)
                return True
        else:
            self._already_alerted.discard(src_ip)
        return False


def make_handler(detector: ScanDetector, verbose: bool):
    def handle_packet(pkt) -> None:
        if IP not in pkt or TCP not in pkt:
            return

        src_ip = pkt[IP].src
        dst_port = pkt[TCP].dport

        if verbose:
            print(f"{src_ip} -> {pkt[IP].dst}:{dst_port} [{pkt[TCP].flags}]")

        if detector.record(src_ip, dst_port):
            print(
                f"[ALERT] Possible port scan from {src_ip}: "
                f">= {detector.threshold} distinct ports contacted "
                f"within {detector.window_seconds:.0f}s"
            )

    return handle_packet


def main() -> None:
    parser = argparse.ArgumentParser(description="Live traffic sniffer with scan detection.")
    parser.add_argument("-i", "--interface", required=True, help="Network interface, e.g. eth0")
    parser.add_argument("--threshold", type=int, default=20, help="Distinct ports to trigger an alert")
    parser.add_argument("--window", type=float, default=5.0, help="Sliding time window in seconds")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print every TCP packet seen")
    args = parser.parse_args()

    detector = ScanDetector(threshold=args.threshold, window_seconds=args.window)
    handler = make_handler(detector, args.verbose)

    print(f"Sniffing on {args.interface}... (Ctrl+C to stop)")
    sniff(iface=args.interface, prn=handler, store=False)


if __name__ == "__main__":
    main()
