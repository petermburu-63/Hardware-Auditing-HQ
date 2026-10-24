# Project 5: Honeypot Server

**Side:** Defense · **Difficulty:** Mid-High · **Language:** Python

## What is this, in plain English?

A **honeypot** is a fake target you deliberately set up to look valuable and vulnerable — a fake login page, a fake database, a fake file server — with the sole purpose of attracting attackers so you can **watch what they do** without any real risk, since there's nothing real to steal or break. Think of it as a decoy car left unlocked with a hidden camera on it, instead of your actual car.

## Why it matters

- Honeypots are a real, widely-used defensive strategy. Companies deploy them inside their networks specifically to detect attackers who've already gotten past the perimeter — any traffic hitting the honeypot is automatically suspicious, since nobody has a legitimate reason to connect to a server that doesn't actually do anything.
- They're also a research tool: security researchers run honeypots exposed to the open internet just to collect data on what attacks are currently popular, what passwords are being tried, what exploits are circulating.
- Building one teaches you both sides at once: you have to understand what makes a service *look* real and tempting to understand what to fake.

## How it actually works

1. **Pick a service to impersonate** — SSH and a basic web login form are the classic beginner choices because they're the most commonly attacked.
2. **Build a fake version** that accepts connections and *looks* functional:
   - A fake SSH server that accepts any username/password, logs the attempt, then disconnects (or pretends to grant access to a fake shell).
   - A fake web login page that accepts any credentials, logs them, and shows a believable "login failed" or redirects to a fake dashboard.
3. **Log everything**: source IP, timestamp, username/password tried, any commands typed if you're faking a shell. This log is the entire point — it's your record of "who's trying to break in and how."
4. **Never let it touch anything real**: the honeypot must be fully isolated — no real data, no real credentials, no network path to anything that matters. Typically run in its own VM or container with no access to your real systems.
5. **Analyze the data**: after running for a while, look at patterns — which usernames/passwords are tried most? Are the same IPs coming back? Do attacks spike at certain times?

## Build it yourself (core pieces)

- A fake SSH honeypot is a great starting project — libraries like `paramiko` (Python) let you implement just enough of the SSH protocol to accept connections and log credentials without actually authenticating anyone.
- A fake web login is even simpler: a basic Flask app with a login form that always logs the attempt and always shows "invalid credentials."
- Add fake "bait": give your fake shell a few believable fake files and directories (`config.txt`, `backup.sql`) to see if attackers poke around further once "in."
- Consider running it on a cheap cloud VM exposed to the real internet (fully isolated, nothing of value on it) — you'll be surprised how fast random scanning bots from across the internet start hitting it, often within minutes.

## Where to practice safely

- Run honeypots only on machines/accounts you own, fully isolated from anything real.
- If you expose one to the public internet, make sure it's on a throwaway VM with zero real data, zero real credentials reused anywhere, and no network path back into anything you care about.
