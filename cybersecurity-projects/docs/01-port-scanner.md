# Project 1: Port & Service Scanner

**Side:** Offense (reconnaissance) · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

Every computer on a network has "ports" — think of them like numbered doors on a building. Port 80 is usually the door for a website, port 22 is usually the door for remote login (SSH), port 3306 is usually a database, and so on. A **port scanner** walks up to a target machine and knocks on a range of doors to see which ones answer. If a door answers, something is listening behind it — and that "something" might be insecure, outdated, or misconfigured.

This is the very first thing both attackers and professional penetration testers do: **map out what's actually running** before deciding what to target. You can't attack or defend what you don't know exists.

## Why it matters

- Companies run these scans on their *own* networks constantly to find things they forgot about (an old test server still exposed to the internet, a database port left open by accident).
- Attackers run the exact same kind of scan to find an easy way in.
- It's the foundation skill behind almost every other offensive security tool — vulnerability scanners, exploit frameworks, and recon tools all start here.

## How it actually works

1. **Pick a target** (an IP address or hostname) and a range of ports to check (e.g., 1–1024, the "well-known" ports).
2. For each port, try to open a network connection (a TCP "handshake"). There are a few ways to do this:
   - **Connect scan**: fully complete the handshake — reliable but noisy (easy to detect/log).
   - **SYN scan ("half-open")**: send the first handshake packet and see if you get a reply, then back out before finishing — faster and quieter, but requires raw socket access.
3. If the port replies, it's **open**. If it refuses, it's **closed**. If nothing replies at all, it's likely **filtered** by a firewall.
4. For open ports, try **banner grabbing** — read the first message the service sends back, which often reveals exactly what software and version is running (e.g., "OpenSSH 8.2").
5. Output a clean report: IP, open ports, service name, version if found.

## Build it yourself (core pieces)

- Python's built-in `socket` library is enough for a basic connect scan.
- Use `threading` or `asyncio` so you're not scanning one port at a time (scanning 65,535 ports one-by-one would take forever).
- Add a simple banner-grab: after connecting, try reading a few bytes the service sends on its own.
- Stretch goal: compare your results against `nmap -sV` run on the same target and see how close you get.

## Where to practice safely

- Your own home lab VMs
- TryHackMe or Hack The Box (both explicitly allow scanning their lab machines)
- **Never** scan IPs you don't own or have written permission to test — in some jurisdictions, unauthorized scanning alone can be treated as a crime, even without further action.
