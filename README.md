# Hardware Audit HQ

A professional lab repository for measuring device posture, telemetry exposure, and system hardening across consumer and enterprise hardware.

## Mission

Hardware Audit HQ exists to combine practical hardware review, software behavior analysis, and security-minded system auditing into one structured workspace. The goal is to understand what a device is really doing in context, not just what the marketing material says it should do.

## Core areas

### 1. Device reconnaissance
- hardware inventory and baseline mapping
- BIOS / firmware posture review
- boot configuration and platform trust review
- operating system baseline comparison

### 2. Performance and stability review
- thermal and power behavior under load
- responsiveness and throttling analysis
- synthetic workload characterization
- reliability and drift tracking over time

### 3. Security and hardening review
- service exposure and telemetry review
- configuration drift analysis
- risk-oriented notes and remediation guidance
- structured comparison against best-practice baselines

## Repository structure

```text
Hardware-Auditing-HQ/
├── README.md
├── LICENSE
├── cybersecurity-projects/
│   ├── README.md
│   ├── requirements.txt
│   ├── offense/
│   │   ├── 01_port_scanner.py
│   │   ├── 02_packet_sniffer.py
│   │   ├── 03_hash_cracker.py
│   │   ├── 08_vuln_scanner.py
│   │   ├── advanced_recon_suite.py
│   │   └── README.md
│   ├── defense/
│   │   ├── 04_hids.py
│   │   ├── 05_honeypot.py
│   │   ├── 06_phishing_detector.py
│   │   ├── 07_file_integrity_monitor.py
│   │   ├── 09_mini_siem.py
│   │   ├── 10_encrypted_vault.py
│   │   ├── README.md
│   │   └── host_monitor.py
│   ├── docs/
│   │   ├── README.md
│   │   └── SECURITY_LAB_GUIDE.md
│   └── analytics/
│       └── telemetry_analyzer.py
├── telemetry_dumps/
└── notes/
```

## Methodology

The work in this repo follows a measurement-first approach:

- measure before judging
- document configuration and state clearly
- compare expected behavior with observed behavior
- record findings with evidence, not assumptions
- treat hardening as a continuous process

## Ethical use and scope

This repository is intended for:

- personal lab environments
- authorized testing scenarios
- educational analysis
- controlled home-lab or enterprise demo environments

Do not run the scripts here against systems you do not own or do not have explicit permission to test.

## Learning flow

1. Reconnaissance and service discovery
2. Baseline security telemetry review
3. Defensive monitoring and change tracking
4. Device and host-level risk interpretation
5. Hardening recommendations and evidence-based reporting

## Operational stance

This project is built to look and function like a serious security engineering workspace, but it remains educational, evidence-focused, and safe by design.

## Writer

Peter Mburu

- AS I ALWAYS SAY GITGOOD -
