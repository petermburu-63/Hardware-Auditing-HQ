# Cybersecurity Projects — Learn by Building

10 hands-on projects covering both **offense** (how attackers think) and **defense** (how to stop them). Each one has its own explainer written for someone who isn't already a security expert — what it does, why it matters, and how it actually works under the hood.

**Rule for all of these:** only scan, attack, or test systems you own or have written permission to test (your own VMs, a home lab, or a legal platform like Hack The Box / TryHackMe). Doing this against someone else's systems without permission is illegal in most countries.

## The Projects

| # | Project | Side | Difficulty |
|---|---------|------|------------|
| 1 | [Port & Service Scanner](projects/01-port-scanner.md) | Offense (recon) | Mid |
| 2 | [Packet Sniffer & Traffic Analyzer](projects/02-packet-sniffer.md) | Both | Mid |
| 3 | [Password Hash Cracker](projects/03-hash-cracker.md) | Offense | Mid |
| 4 | [Host-Based Intrusion Detection System](projects/04-hids.md) | Defense | High |
| 5 | [Honeypot Server](projects/05-honeypot.md) | Defense | Mid-High |
| 6 | [Phishing URL Detector (ML)](projects/06-phishing-detector.md) | Defense | High |
| 7 | [File Integrity Monitor](projects/07-file-integrity-monitor.md) | Defense | Mid |
| 8 | [Vulnerability Scanner](projects/08-vuln-scanner.md) | Offense | High |
| 9 | [Mini SIEM / Log Correlation Engine](projects/09-mini-siem.md) | Defense | High |
| 10 | [Encrypted File Vault](projects/10-encrypted-vault.md) | Defense (crypto) | Mid |

Each explainer links to a matching, runnable starter implementation in [`code/`](code/) (same number prefix, e.g. `01-port-scanner.md` ↔ `code/01_port_scanner.py`). Install dependencies with `pip install -r requirements.txt`.

## Suggested order
If you want a natural progression: **1 → 2 → 7 → 3 → 5 → 4 → 9 → 6 → 8 → 10**. Recon basics first, then defense fundamentals, then the harder stuff (ML, correlation engines, full vuln scanning).

## What you'll need
- Python 3.10+ for almost everything here
- A home lab: a couple of cheap VMs (VirtualBox/VMware/Proxmox) is enough — never test tools on networks or machines you don't own
- Optional but great: a Kali Linux VM as your "attacker box" and an Ubuntu/Windows VM as your "target"
