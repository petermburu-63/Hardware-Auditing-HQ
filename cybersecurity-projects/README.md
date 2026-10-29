# Cybersecurity Projects

This project area is structured as a practical security engineering workspace. It combines discovery, defensive monitoring, and telemetry analysis into a coherent training model for students, lab users, and security-minded engineers.

## Project objectives

The repository covers five major operating themes:

1. Reconnaissance and service discovery
2. Behavioral and network-level anomaly review
3. Defensive monitoring and change tracking
4. Telemetry correlation and risk detection
5. Evidence-driven reporting and hardening guidance

## Repository map

```text
cybersecurity-projects/
├── README.md
├── requirements.txt
├── offense/
│   ├── 01_port_scanner.py
│   ├── 02_packet_sniffer.py
│   ├── 03_hash_cracker.py
│   ├── 08_vuln_scanner.py
│   ├── advanced_recon_suite.py
│   ├── host_discovery_engine.py
│   ├── advanced_service_mapper.py
│   └── README.md
├── defense/
│   ├── 04_hids.py
│   ├── 05_honeypot.py
│   ├── 06_phishing_detector.py
│   ├── 07_file_integrity_monitor.py
│   ├── 09_mini_siem.py
│   ├── 10_encrypted_vault.py
│   ├── host_monitor.py
│   ├── host_guard.py
│   └── README.md
├── analytics/
│   ├── telemetry_analyzer.py
│   └── risk_index.py
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── PROJECT_BLUEPRINT.md
│   └── SECURITY_LAB_GUIDE.md
└── telemetry/
```

## Design principles

- Clear separation between offense, defense, and analytics
- Reusable CLI structure across project scripts
- Honest educational framing and safety notes
- Realistic but lab-safe security tool patterns
- Output designed for reporting and automation

## Learning flow

1. Host and service discovery
2. Service mapping and banner review
3. Telemetry and log interpretation
4. Defensive monitoring and integrity verification
5. Risk summary and hardening reporting

## Safety and responsibility

The scripts in this section are intended for:

- controlled lab systems
- private test environments
- authorized internal review
- educational demos

They are not intended for outside or unauthorized use.

## Requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Typical usage

```bash
python3 cybersecurity-projects/offense/host_discovery_engine.py --host 192.168.1.10 --ports 1-1024 --json
python3 cybersecurity-projects/offense/advanced_service_mapper.py --host 192.168.1.10 --ports 22,80,443,8080
python3 cybersecurity-projects/analytics/risk_index.py --events telemetry/example-events.json
python3 cybersecurity-projects/defense/host_guard.py --path /tmp/lab-monitor --interval 5 --iterations 3
```
