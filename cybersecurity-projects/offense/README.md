# Cybersecurity Projects

A hands-on collection of security labs designed to teach the same ideas used in real-world security engineering: discovery, monitoring, defense, and protection.

This stack is built for two audiences:
- Technical people who want the actual code and logic.
- Non-technical readers who want a clear, plain-English explanation of what each lab is doing and why it matters.

## The core idea

Each project is an intentionally small, understandable security tool. Together they form a practical learning path from reconnaissance to detection to protection.

## How to read this repo

- Offense: projects that model how attackers or security researchers discover systems and weaknesses.
- Defense: projects that monitor, detect, trap, and protect systems.
- Analytics: projects that interpret patterns and classify risk.
- Docs: explanations written to make the work approachable without losing technical depth.

## Quick safety note

Only test systems you own or have explicit permission to test. These scripts are educational and should be run in controlled lab environments such as a home lab, a VM, or a legal training platform.

## Project categories

### Offense

- Recon and discovery
- Network scanning
- Service fingerprinting
- Hash cracking exercises
- Vulnerability lookups

### Defense

- HIDS monitoring
- File integrity checks
- Honeypots
- SIEM-style event correlation
- Encryption and safe storage

### Analytics

- Phishing detection using a lightweight ML model
- Pattern recognition over suspicious activity

### Docs

- Plain-English project explainers
- Milestone walkthroughs
- Safety and usage notes

## Suggested learning order

1. Recon: port scanning and packet analysis
2. Baseline defense: file integrity monitoring
3. Brute-force detection: HIDS
4. SIEM logic: log correlation
5. ML and phishing detection
6. Vulnerability lookups and scanning
7. Encryption and protected storage

## Requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Repository footprint

- `offense/` - offensive and reconnaissance-oriented projects
- `defense/` - defensive and monitoring projects
- `analytics/` - ML and risk classification projects
- `docs/` - security explainers and project notes
- `requirements.txt` - Python dependencies

## Who this is for

This repo is ideal for:
- students learning security fundamentals
- developers who want to understand how attacks and defense work in practice
- IT/security hobbyists building a lab in a safe environment
- anyone curious about how modern security tooling actually works

## Important framing

These projects are not meant to be malicious automation. They are intentionally designed to teach understanding, detection, and defense. The most valuable skill in cybersecurity is not brute-force access. It is the ability to reason clearly about risk, systems, and controls.
