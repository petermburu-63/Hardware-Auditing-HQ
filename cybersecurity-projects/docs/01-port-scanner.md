# Project 1: Port & Service Scanner

**Side:** Offense (reconnaissance) · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

Every computer on a network has "ports". Think of them like numbered doors on a building. Port 80 is usually the door for a website, port 22 is usually the door for remote login (SSH), port 3306 is usually a database, and so on. A port scanner walks up to a target machine and knocks on a range of doors to see which ones answer. If a door answers, something is listening behind it. That "something" might be insecure, outdated, or misconfigured.

This is the very first thing both attackers and professional penetration testers do: map out what is actually running before deciding what to target. You cannot attack or defend what you do not know exists.

## Why it matters

- Companies run these scans on their own networks constantly to find things they forgot about, such as an old test server still exposed to the internet or a database port left open by accident.
- Attackers run the exact same kind of scan to find an easy way in.
- It is the foundation skill behind almost every other offensive security tool, including vulnerability scanners, exploit frameworks, and recon tools.

## How it actually works

1. Pick a target, such as an IP address or hostname, and a range of ports to check, such as 1 to 1024 or the well-known ports.
2. For each port, try to open a network connection, which is a TCP handshake. There are a few ways to do this:
   - Connect scan: fully complete the handshake. It is reliable but noisy and easy to detect.
   - SYN scan, or half-open scan: send the first handshake packet and see if you get a reply, then back out before finishing. It is faster and quieter, but it requires raw socket access.
3. If the port replies, it is open. If it refuses, it is closed. If nothing replies at all, it is likely filtered by a firewall.
4. For open ports, try banner grabbing. Read the first message the service sends back, which often reveals exactly what software and version is running, such as OpenSSH 8.2.
5. Output a clean report: IP, open ports, service name, and version if found.

## Build it yourself (core pieces)

- Python's built-in `socket` library is enough for a basic connect scan.
- Use `threading` or `asyncio` so you are not scanning one port at a time. Scanning 65,535 ports one by one would take forever.
- Add a simple banner grab. After connecting, try reading a few bytes the service sends on its own.
- Stretch goal: compare your results against `nmap -sV` run on the same target and see how close you get.

## Where to practice safely

- Your own home lab VMs
- TryHackMe or Hack The Box, which explicitly allow scanning their lab machines
- Never scan IPs you do not own or have written permission to test. In some jurisdictions, unauthorized scanning alone can be treated as a crime, even without further action.
