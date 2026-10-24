# Project 8: Vulnerability Scanner

**Side:** Offense (with defensive use) · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

Once you know what is running on a machine, a vulnerability scanner goes a step further and checks whether that specific software has known security holes. It is the difference between seeing a door and knowing that this exact lock model has a published flaw that lets you pick it in 10 seconds.

## Why it matters

- This is the real, professional version of "hacking" most people imagine, but it is also used constantly by defenders.
- It directly teaches you about CVEs, the public, standardized database the entire security industry uses to track known flaws in software versions.
- Building one, even a simple one, teaches you how tools like Nessus, OpenVAS, and Nmap's vulnerability scripts actually work.

## How it actually works

1. Fingerprint the target: identify exactly what software and version is running.
2. Look up known vulnerabilities: take that exact software and version and check it against a vulnerability database such as the NVD.
3. Match and report: if the target is running vulnerable software, flag it and include a severity score.
4. Optionally verify: for well-understood vulnerabilities, write a safe, non-destructive check that confirms the flaw is actually present.
5. Report: produce a clear output with target details, software detected, CVEs matched, and severity.

## Build it yourself (core pieces)

- Combine banner grabbing with the NVD's public API.
- Start narrow: pick one specific software and build a scanner that detects just that one thing well.
- A good mid-level goal is to correctly identify the software and version and pull back a list of matching CVEs with severity.
- Stretch goal: write one safe checker for a well-known non-destructive vulnerability rather than anything that could damage the target.

## Where to practice safely

- Only run this against your own lab VMs with deliberately outdated or vulnerable software installed for practice.
- Actual exploitation of a found vulnerability against anything you do not own crosses a legal line. Detection and reporting is the safe, legal skill to focus on.
