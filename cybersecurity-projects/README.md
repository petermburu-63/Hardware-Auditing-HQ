# Cybersecurity Projects

This project area is a structured security engineering workspace designed to teach realistic operational techniques while staying within a controlled, ethical, and lab-safe scope.

## Project goals

The repository covers several major domains:

1. Reconnaissance and service discovery
2. Behavioral and network anomaly review
3. Defensive monitoring and integrity tracking
4. Telemetry correlation and risk detection
5. Evidence-based reporting and hardening guidance

## Repository flow

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
│   ├── PROJECT_ROADMAP.md
│   ├── SECURITY_LAB_GUIDE.md
│   └── scenarios/
│       └── advanced-lab-scenarios.md
└── telemetry/
```

## Why these tools matter

These scripts are useful because they demonstrate the real patterns behind operational security work:

- discovery and exposure review
- telemetry signal classification
- baseline monitoring and change detection
- risk summary and documentation
- evidence-driven remediation recommendations

## Learning flow

1. Host and service discovery
2. Service mapping and banner review
3. Telemetry and log interpretation
4. Defensive monitoring and integrity verification
5. Risk summary and hardening reporting

## Research notebook

The workspace also includes a research notebook for deeper case analysis and journaling.

## Safety and responsibility

The scripts here are intended for:

- private lab systems
- controlled review environments
- educational and training use
- authorized internal testing

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
