# Project 9: Mini SIEM / Log Correlation Engine

**Side:** Defense · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

A SIEM, or Security Information and Event Management system, is the central nervous system of a real security team. It pulls in logs from every machine, firewall, and application across an organization and looks for patterns that no single log alone would reveal.

One failed login on one server is nothing. But one failed login on ten different servers within 30 seconds, all from the same external IP, is a coordinated attack. You only see that by looking across all the logs together.

## Why it matters

- Real SIEMs such as Splunk, Elastic Security, and Microsoft Sentinel are the backbone tools of nearly every security operations center.
- It teaches correlation, which is the actual hard, interesting problem in defensive security: not just did something bad happen, but do these separate events together mean something bad is happening.
- It naturally pulls together many other project ideas: network detection, HIDS alerts, FIM warnings, and auth logs.

## How it actually works

1. Ingest: collect logs from multiple sources into one place and normalize them into a common format.
2. Store: put normalized events into a simple database such as SQLite or a proper time-series store.
3. Correlate: write rules that span multiple events.
   - same source IP failing login on several hosts within a short window
   - file integrity alert followed by a new outbound connection
   - spike in failed logins followed by one success
4. Score and prioritize: not every alert matters equally.
5. Visualize and report: show recent alerts, top offending IPs, and a timeline.

## Build it yourself (core pieces)

- SQLite plus Python is enough to prototype the whole thing.
- Design your common event format first: timestamp, source host, event type, details.
- Start with just one correlation rule and get it working end to end before adding more.
- A simple Flask dashboard showing alerts in the last 24 hours is a great visible deliverable.

## Where to practice safely

- Entirely safe. You are writing a log analysis tool, not attacking anything.
- Feed it logs from your own lab VMs to test it realistically.
