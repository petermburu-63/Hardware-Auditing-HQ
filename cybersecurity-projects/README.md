# Cybersecurity Projects

This folder contains a structured collection of security engineering exercises designed to teach the mechanics of discovery, monitoring, and defensive analysis in a realistic lab environment.

## The idea

Each project is intentionally small but realistic. Together they form a practical progression from reconnaissance to detection to defense. The work is meant to be clear enough for students while still closely resembling the shapes and structure of professional tooling.

## How to read this repo

- Offense: discovery, fingerprinting, scanning, and service interrogation
- Defense: monitoring, integrity tracking, alerting, and response logic
- Analytics: telemetry review, pattern interpretation, and operational reporting
- Docs: explanation and walkthrough material for safe learning

## Safety and ethics

Only test systems you own or are explicitly authorized to assess. Use these scripts in a controlled lab, personal network, or training environment.

## Project categories

### Offense
- port scanning and banner collection
- packet inspection and anomaly review
- hash analysis and password-policy exercises
- service and vulnerability lookup workflows

### Defense
- host-based detection rules
- file integrity monitoring
- honeypot-style deception patterns
- SIEM-style event correlation
- encrypted vault and secure storage patterns

### Analytics
- suspicious activity summaries
- log normalization and alerting heuristics
- telemetry trend review
- operational reporting workflows

### Docs
- explainers and project walkthroughs
- lab safety and usage notes
- best-practice operational framing

## Suggested learning order

1. Reconnaissance and service discovery
2. Traffic and packet review
3. Defensive correlation and alerting
4. Telemetry review and suspicious-pattern analysis
5. Risk framing and reporting

## Requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Repository footprint

- offense/: offensive and reconnaissance-oriented tools
- defense/: defensive monitoring and protection scripts
- analytics/: telemetry parsing and suspicious activity detection
- docs/: guides and architectural notes
- requirements.txt: dependency list for the lab stack
