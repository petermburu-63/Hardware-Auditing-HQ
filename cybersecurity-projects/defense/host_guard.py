#!/usr/bin/env python3
"""Advanced Service Mapper

Maps discovered services to a higher-level application profile and summarizes
what is likely exposed on a target. This is educational and should be used only
in controlled environments.
"""

from __future__ import annotations

import argparse
import socket
import ssl
from dataclasses import dataclass
from typing import Iterable


@dataclass
class ServiceProfile:
    port: int
    name: str
    confidence: str
    summary: str


SERVICE_MAPPINGS = {
    21: ("ftp", "low", "File transfer service commonly exposed on internal or edge servers."),
    22: ("ssh", "high", "Secure shell endpoint for remote administration."),
    23: ("telnet", "medium", "Legacy cleartext remote access service."),
    25: ("smtp", "medium", "Mail submission or relay service."),
    53: ("dns", "high", "Domain name resolution service."),
    80: ("http", "high", "Web service reachable over plaintext HTTP."),
    110: ("pop3", "low", "Mailbox access over a legacy protocol."),
    143: ("imap", "medium", "Mailbox access and synchronization service."),
    443: ("https", "high", "Secure web service protected by TLS."),
    465: ("smtps", "medium", "SMTP over TLS, often used for submission."),
    993: ("imaps", "medium", "IMAP protected with TLS."),
    3306: ("mysql", "medium", "Structured database service."),
    5432: ("postgresql", "medium", "Relational database backend."),
    8080: ("http-alt", "medium", "Alternate HTTP listener commonly used by web apps."),
    8443: ("https-alt", "medium", "Alternate HTTPS listener commonly used by web apps."),
}


def inspect_banner(host: str, port: int, timeout: float = 1.0) -> str | None:
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(b"\n")
            data = sock.recv(512)
            return data.decode(errors="replace").strip() or None
    except (socket.timeout, OSError):
        return None


def tls_probe(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.create_connection((host, port), timeout=timeout), server_hostname=host) as sock:
            sock.settimeout(timeout)
            return True
    except Exception:
        return False


def profile_service(host: str, port: int) -> ServiceProfile:
    name, confidence, summary = SERVICE_MAPPINGS.get(port, ("unknown", "low", "Unclassified or custom service."))
    banner = inspect_banner(host, port)

    if port in (443, 8443) and tls_probe(host, port):
        name = "https" if port == 443 else "https-alt"
        summary = "TLS-protected application endpoint detected." if not banner else summary

    if banner:
        banner_text = banner.replace("\r", " ").replace("\n", " ").strip()
        if len(banner_text) > 160:
            banner_text = banner_text[:157] + "..."
        summary = f"Service banner indicates: {banner_text}"

    return ServiceProfile(port=port, name=name, confidence=confidence, summary=summary)


def map_services(host: str, ports: Iterable[int]) -> list[ServiceProfile]:
    return [profile_service(host, port) for port in ports]


def main() -> None:
    parser = argparse.ArgumentParser(description="Map open ports to high-level application services.")
    parser.add_argument("--host", required=True, help="Target host or IP")
    parser.add_argument("--ports", default="22,80,443,8080", help="Comma-separated port list")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds")
    args = parser.parse_args()

    ports = [int(part.strip()) for part in args.ports.split(",") if part.strip()]
    for profile in map_services(args.host, ports):
        print(f"Port {profile.port}: {profile.name} ({profile.confidence})")
        print(f"  - {profile.summary}")


if __name__ == "__main__":
    main()
