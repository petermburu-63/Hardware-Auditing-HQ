# Hardware-Audit-HQ

A practical lab for auditing hardware, software posture, telemetry exposure, and system hardening across consumer and enterprise devices.

This repository is built around one idea: if a device is going to be trusted in a real environment, it should be measured, documented, and tested with a critical eye.

I use this space to document device reconnaissance, performance behavior, thermal characteristics, firmware posture, telemetry risk, and hardening opportunities. The goal is to move beyond marketing specs and look at what the hardware and operating system are actually doing.

## What this repo covers

### Device reconnaissance

- hardware inventory and baseline mapping
- BIOS and UEFI review
- boot security and firmware posture
- operating system baseline comparison

### Performance and stability analysis

- thermal throttling observations
- power draw and efficiency review
- synthetic workload behavior
- system responsiveness under sustained load

### Security and hardening review

- telemetry exposure and unnecessary background activity
- service and configuration review
- baseline drift analysis
- compliance-minded hardening notes

## Repository structure

- `/Recon` — hardware and system reconnaissance notes, configuration findings, and baseline data
- `/Stress-Tests` — benchmarking, thermal, power, and workload analysis
- `/Audit-Findings` — security observations, risk notes, and hardening recommendations
- `/telemetry_dumps` — captured telemetry and system data for review and comparison

## Why this exists

Most hardware reviews stop at specs and benchmarks. This repo goes a bit further and asks a more useful question: what is this system really doing, how stable is it under load, and what security or privacy tradeoffs are baked in?

This is useful for:

- IT auditing work
- security-focused system review
- hardware benchmarking and baseline tracking
- understanding how telemetry and software behavior affect trust in a device

## Methodology

The work here is guided by practical auditing principles:

- measure before judging
- document configuration and state clearly
- compare expected behavior with observed behavior
- log findings with evidence, not assumptions
- treat hardening as a continuous process, not a one-time checklist

## Scope and use

This repository is for educational and lab use. It is intended for structured review of personal, lab, and test systems under controlled conditions.

All activity in this repository is aligned with responsible testing practices, local compliance expectations, and ethical system review.

## Status

Operational

## Lead

Peter Mburu
