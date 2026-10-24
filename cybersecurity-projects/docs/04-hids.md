# Project 4: Host-Based Intrusion Detection System (HIDS)

**Side:** Defense · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

An **Intrusion Detection System** watches a computer for signs that someone is doing something they shouldn't — and raises an alarm. A **host-based** one (as opposed to network-based) watches *one specific machine* from the inside: its logs, its running processes, its file changes, its login attempts. Think of it as a security guard who lives inside the building and notices when something's off, rather than one watching the front gate.

## Why it matters

- This is the core idea behind real products like OSSEC, Wazuh, and the "EDR" (Endpoint Detection and Response) tools that companies pay serious money for.
- Attackers who get past the front door (firewalls, login screens) still have to *do things* on the machine — and those actions leave traces. A HIDS is what catches them after the perimeter has already failed.
- It teaches you to think like a defender: not "how do I stop every attack" (impossible) but "how do I notice when one is happening."

## How it actually works

A HIDS is really a collection of smaller watchers, each looking for a different kind of trouble:

1. **Log monitoring**: tail system/auth logs (e.g., `/var/log/auth.log` on Linux) and flag patterns like 10 failed SSH login attempts in 60 seconds from the same IP (classic brute-force signature).
2. **File integrity monitoring**: hash important files (system binaries, config files) periodically and alert if the hash changes unexpectedly — a changed `/etc/passwd` or `/bin/ls` is a huge red flag (see Project 7 for a deep dive on this specific piece).
3. **Process monitoring**: keep a baseline list of what normally runs on this machine, and alert on anything new and unrecognized — especially processes with suspicious names or running from unusual locations like `/tmp`.
4. **Network connection monitoring**: watch for the machine making outbound connections to known-bad IPs or unusual ports (could indicate malware "phoning home" to its controller).
5. **Alerting**: when a rule triggers, do something — write to an alert log, send an email/Slack message, or (in a mini-SIEM setup, see Project 9) forward the event for correlation with other machines.

## Build it yourself (core pieces)

- Start with just the log-monitoring piece: write a script that tails `auth.log` and counts failed logins per IP in a rolling time window.
- Add file integrity checks using the hashing logic from Project 7.
- Add a simple rules engine: a config file where you define "if X happens Y times in Z seconds, alert" — this pattern (threshold-based detection) is the backbone of almost all real detection systems.
- Stretch goal: when an alert fires, automatically take a defensive action, like blocking the offending IP with the local firewall (`iptables`/`ufw`) — now you've built a baby version of an "IPS" (Intrusion *Prevention* System).

## Where to practice safely

- Build and test this entirely on your own home lab VM.
- To generate test data, do a *controlled* brute-force against your own test VM's SSH (e.g., using `hydra` with a short list against a throwaway account you made specifically for this) so you have real failed-login logs to detect.
