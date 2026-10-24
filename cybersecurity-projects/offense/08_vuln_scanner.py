#!/usr/bin/env python3
"""
Vulnerability Scanner (banner-based, CVE lookup only)
---------------------------------------------------------
Grabs a service banner from a port and queries the public NVD
(National Vulnerability Database) API for known CVEs matching that
product/version string. This script only DETECTS and REPORTS —
it never attempts to exploit anything.

Requires: requests   (pip install requests)

Usage:
    python3 08_vuln_scanner.py --host 192.168.1.10 --port 22
    python3 08_vuln_scanner.py --host 192.168.1.10 --port 80 --product "apache http server" --version "2.4.49"

Only run this against systems you own or have written permission to test.
"""

from __future__ import annotations

import argparse
import re
import socket
import time

import requests

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

BANNER_PATTERNS = [
    re.compile(r"SSH-\d\.\d-OpenSSH_(?P<version>[\w.]+)"),
    re.compile(r"Server: (?P<product>Apache)/(?P<version>[\d.]+)", re.IGNORECASE),
    re.compile(r"Server: (?P<product>nginx)/(?P<version>[\d.]+)", re.IGNORECASE),
]


def grab_banner(host: str, port: int, timeout: float = 3.0) -> str:
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            if port in (80, 8080, 8000):
                sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            data = sock.recv(1024)
            return data.decode(errors="replace")
    except OSError as exc:
        raise SystemExit(f"Could not connect to {host}:{port} — {exc}")


def parse_product_version(banner: str) -> tuple[str | None, str | None]:
    for pattern in BANNER_PATTERNS:
        match = pattern.search(banner)
        if match:
            groups = match.groupdict()
            product = groups.get("product", "OpenSSH" if "OpenSSH" in banner else None)
            return product, groups.get("version")
    return None, None


def query_nvd(product: str, version: str, api_key: str | None = None) -> list[dict]:
    """Query the NVD API for CVEs mentioning this product+version, politely rate-limited."""
    headers = {"apiKey": api_key} if api_key else {}
    params = {"keywordSearch": f"{product} {version}", "resultsPerPage": 20}

    response = requests.get(NVD_API_URL, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("vulnerabilities", []):
        cve = item["cve"]
        cve_id = cve["id"]
        description = next(
            (d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"),
            "(no description)",
        )
        metrics = cve.get("metrics", {})
        severity = "UNKNOWN"
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if key in metrics:
                severity = metrics[key][0]["cvssData"].get("baseSeverity", "UNKNOWN")
                break

        results.append({"id": cve_id, "severity": severity, "description": description})

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Banner-based CVE scanner (detection only, no exploitation).")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--product", help="Override auto-detected product name")
    parser.add_argument("--version", help="Override auto-detected version")
    parser.add_argument("--api-key", help="Optional NVD API key (raises your rate limit)")
    args = parser.parse_args()

    product, version = args.product, args.version

    if not (product and version):
        print(f"Grabbing banner from {args.host}:{args.port} ...")
        banner = grab_banner(args.host, args.port)
        print(f"Banner: {banner.splitlines()[0] if banner else '(empty)'}")
        detected_product, detected_version = parse_product_version(banner)
        product = product or detected_product
        version = version or detected_version

    if not (product and version):
        raise SystemExit(
            "Could not auto-detect product/version from the banner. "
            "Re-run with --product and --version explicitly."
        )

    print(f"Looking up CVEs for: {product} {version} ...")
    time.sleep(0.5)

    try:
        cves = query_nvd(product, version, args.api_key)
    except requests.RequestException as exc:
        raise SystemExit(f"NVD lookup failed: {exc}")

    if not cves:
        print("No matching CVEs found (or NVD's keyword match was too broad/narrow — try adjusting terms).")
        return

    print(f"\nFound {len(cves)} potentially related CVE(s):\n")
    for cve in cves:
        print(f"[{cve['severity']:<8}] {cve['id']}")
        print(f"            {cve['description'][:160]}...")
        print()


if __name__ == "__main__":
    main()
