# Project 8: Vulnerability Scanner

**Side:** Offense (with defensive use) · **Difficulty:** High · **Language:** Python

## What is this, in plain English?

Once you know what's running on a machine (Project 1 tells you *that* a web server is running, say), a **vulnerability scanner** goes a step further and checks *whether that specific software has known security holes*. It's the difference between "I see a door" and "I see a door, and I know this exact lock model has a published flaw that lets you pick it in 10 seconds."

## Why it matters

- This is the real, professional version of "hacking" most people imagine — but it's used constantly by defenders too: companies run vulnerability scans against their *own* infrastructure to find and patch problems before an attacker finds them first.
- It directly teaches you about **CVEs** (Common Vulnerabilities and Exposures) — the public, standardized database the entire security industry uses to track known flaws in specific software versions.
- Building one, even a simple one, teaches you how tools like Nessus, OpenVAS, and Nmap's vulnerability scripts actually work instead of just running them as a black box.

## How it actually works

1. **Fingerprint the target**: identify exactly what software and version is running (this is the banner-grabbing step from Project 1, done thoroughly — e.g., "Apache 2.4.49" not just "a web server").
2. **Look up known vulnerabilities**: take that exact software+version and check it against a vulnerability database. The National Vulnerability Database (NVD) publishes a free, searchable API of every known CVE, including which software versions are affected.
3. **Match and report**: if the target is running Apache 2.4.49, and the database shows CVE-2021-41773 (a real, famous path traversal bug) affects exactly that version, flag it — with a severity score (CVSS) telling you how bad it is.
4. **Optionally verify**: for well-understood vulnerabilities, write a safe, non-destructive check that confirms the flaw is actually present and not just "the version number matches" (version numbers can be misleading if a vendor backported a fix without changing the version string).
5. **Report**: produce a clear output — target, software detected, CVEs matched, severity, and ideally a one-line description of the risk and the fix (usually "upgrade to version X").

## Build it yourself (core pieces)

- Combine Project 1's banner-grabbing with the **NVD's public API** (`services.nvd.nist.gov`) which lets you query CVEs by product/version for free.
- Start narrow: pick one specific, well-documented software (e.g., a specific old WordPress or Apache version) and build a scanner that detects just that one thing really well, rather than trying to cover everything at once.
- A good mid-level goal: given a target's HTTP response headers and banners, correctly identify the server software/version and pull back a list of matching CVEs with severity scores.
- Stretch goal: write one single, safe "checker" for a specific, well-known, non-destructive vulnerability (e.g., checking if a specific misconfigured endpoint returns something it shouldn't) rather than anything that could crash or damage the target.

## Where to practice safely

- Only ever run this against your own lab VMs with deliberately outdated/vulnerable software installed for practice (projects like **Metasploitable** and **DVWA** exist specifically for this — they're intentionally vulnerable practice targets).
- Actual exploitation (not just detection) of a found vulnerability against anything you don't own crosses a legal line — detection/reporting is the safe, legal, professional-equivalent skill to focus on.
