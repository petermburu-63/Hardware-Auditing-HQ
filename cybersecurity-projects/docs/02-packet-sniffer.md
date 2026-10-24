# Project 2: Packet Sniffer & Traffic Analyzer

**Side:** Both (recon for offense, monitoring for defense) · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

Every time your computer talks to the internet or another device, it sends data in small chunks called packets. These packets are like letters sent in pieces, with labels showing where they came from and where they are going. A packet sniffer sits on the network and reads every piece of mail going past, even ones not addressed to it, by putting the network card into promiscuous mode, which means it listens to everything instead of just its own traffic.

This is exactly how tools like Wireshark work. You are building a simplified version of one.

## Why it matters

- Defense: Security teams sniff traffic to spot suspicious patterns, such as a machine suddenly talking to a server in another country at 3 AM or sending far more data out than usual.
- Offense: On an insecure network, such as open public WiFi or a company network an attacker has already gotten into, sniffing can expose passwords, session tokens, or sensitive data sent without encryption.
- This is why HTTPS, VPNs, and encrypted protocols exist. They are designed to make sniffed traffic useless to an attacker.

## How it actually works

1. Capture: Open a raw socket or use a library like `scapy` that gets a copy of every packet passing through your network interface.
2. Parse: Each packet has layers, like an onion.
   - Layer 2, Ethernet: MAC addresses, which physical device sent the packet
   - Layer 3, IP: source and destination IP addresses
   - Layer 4, TCP or UDP: which port is involved and what kind of conversation it is
   - Layer 7, application: the actual content, such as an HTTP request or a DNS lookup
3. Analyze: Pull out useful fields such as source and destination, protocol, size, and flags, and either print them live or log them for later.
4. Detect patterns. This is where it becomes a real tool instead of just a toy.
   - unusually large amounts of traffic to one destination, which may indicate data exfiltration
   - plaintext passwords in HTTP traffic, which should be using HTTPS instead
   - repeated connection attempts to many different ports, which is a port scan in progress

## Build it yourself (core pieces)

- `scapy`, a Python library, makes this much easier than raw sockets. It parses packet layers for you.
- Start simple: print the source IP, destination IP, and protocol for every packet seen in 30 seconds.
- Level up: add a rule such as alerting if more than 20 SYN packets go to different ports from the same source within 5 seconds. That is a simple scan detector.
- Stretch goal: write captured packets to a `.pcap` file and open it in Wireshark to compare what you captured with what Wireshark shows.

## Where to practice safely

- Use your own home network and your own devices only.
- Sniffing traffic on a network you do not own or do not have permission to monitor is illegal in most places, even if the intent is just curiosity.
