# Project 4: Host-Based Intrusion Detection System (HIDS)

**Side:** Defense · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

An intrusion detection system watches a computer for signs that someone is doing something they should not do and raises an alarm. A host-based one watches one specific machine from the inside, looking at its logs, running processes, file changes, and login attempts. Think of it as a security guard living inside the building and noticing when something is off, rather than one watching the front gate.

## Why it matters

- This is the core idea behind real products like OSSEC, Wazuh, and EDR tools that companies pay serious money for.
- Attackers who get past the front door still have to do things on the machine, and those actions leave traces. A HIDS is what catches them after the perimeter has already failed.
- It teaches you to think like a defender. The goal is not to stop every attack. The goal is to notice when one is happening.

## How it actually works

A HIDS is really a collection of smaller watchers, each looking for a different kind of trouble.

1. Log monitoring: tail system or auth logs and flag patterns like 10 failed SSH login attempts in 60 seconds from the same IP.
2. File integrity monitoring: hash important files and alert if the hash changes unexpectedly. A changed `/etc/passwd` or `/bin/ls` is a huge red flag.
3. Process monitoring: keep a baseline list of what usually runs on this machine and alert on anything new or unrecognized, especially suspicious names or unusual paths like `/tmp`.
4. Network connection monitoring: watch for the machine making outbound connections to known bad IPs or unusual ports.
5. Alerting: when a rule triggers, write to an alert log, send an email or Slack message, or forward the event to a SIEM for correlation.

## Build it yourself (core pieces)

- Start with just the log-monitoring piece: write a script that tails `auth.log` and counts failed logins per IP in a rolling time window.
- Add file integrity checks using the hashing logic from Project 7.
- Add a simple rules engine: a config file where you define if X happens Y times in Z seconds, alert. This pattern is the backbone of almost all real detection systems.
- Stretch goal: when an alert fires, block the offending IP with a local firewall. That gives you a baby version of an intrusion prevention system.

## Where to practice safely

- Build and test this entirely on your own home lab VM.
- To generate test data, do a controlled brute-force against your own test VM's SSH with a throwaway account so you have real failed login logs to detect.
