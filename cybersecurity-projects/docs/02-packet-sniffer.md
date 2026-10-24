# Project 2: Packet Sniffer & Traffic Analyzer

**Side:** Both (recon for offense, monitoring for defense) · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

Every time your computer talks to the internet or another device, it sends the data in small chunks called **packets** — like sending a letter in pieces, each piece labeled with where it came from and where it's going. A **packet sniffer** sits on the network and reads every piece of mail going past, even ones not addressed to it, by putting the network card into "promiscuous mode" (listen to everything, not just your own traffic).

This is exactly how tools like Wireshark work — you're building a simplified version of one.

## Why it matters

- **Defense**: Security teams sniff traffic to spot suspicious patterns — a machine suddenly talking to a server in another country at 3 AM, or sending way more data out than usual (a sign of data theft).
- **Offense**: On an insecure network (like open public WiFi, or inside a company network an attacker has already gotten into), sniffing can expose passwords, session tokens, or sensitive data sent without encryption.
- This is why HTTPS, VPNs, and encrypted protocols exist — they exist specifically to make sniffed traffic useless to an attacker.

## How it actually works

1. **Capture**: Open a raw socket (or use a library like `scapy`) that gets a copy of every packet passing through your network interface.
2. **Parse**: Each packet has layers, like an onion:
   - Layer 2 (Ethernet): MAC addresses — which physical device sent it
   - Layer 3 (IP): source and destination IP addresses
   - Layer 4 (TCP/UDP): which port, part of a larger conversation
   - Layer 7 (Application): the actual content — HTTP request, DNS lookup, etc.
3. **Analyze**: Pull out useful fields (source/destination, protocol, size, flags) and either print them live or log them for later.
4. **Detect patterns** (this is where it becomes a real tool, not just a toy):
   - Unusually large amounts of traffic to one destination (possible data exfiltration)
   - Plaintext passwords in HTTP traffic (sites that should be using HTTPS but aren't)
   - Repeated connection attempts to many different ports (a port scan in progress — i.e., someone doing Project 1 to *you*)

## Build it yourself (core pieces)

- `scapy` (Python library) makes this dramatically easier than raw sockets — it parses packet layers for you.
- Start simple: print source IP, destination IP, and protocol for every packet seen in 30 seconds.
- Level up: add a rule like "alert if more than 20 SYN packets to different ports from the same source within 5 seconds" — you've just built a simple scan detector.
- Stretch goal: write captured packets to a `.pcap` file and open it in Wireshark to compare what you captured vs. what Wireshark shows.

## Where to practice safely

- Your own home network and your own devices only
- Sniffing traffic on a network you don't own or don't have permission to monitor is illegal (wiretapping laws) in most places, even if the intent is "just curious"
