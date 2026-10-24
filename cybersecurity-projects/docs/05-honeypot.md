# Project 5: Honeypot Server

**Side:** Defense · **Difficulty:** Mid-High · **Language:** Python

## What is this, in plain English?

A honeypot is a fake target deliberately set up to look valuable and vulnerable. It could be a fake login page, a fake database, or a fake file server. The purpose is to attract attackers so you can watch what they do without any real risk, because there is nothing real to steal or break.

Think of it as a decoy car left unlocked with a hidden camera on it instead of your actual car.

## Why it matters

- Honeypots are a real, widely used defensive strategy. Companies deploy them inside their networks specifically to detect attackers who have already gotten past the perimeter.
- They are also a research tool. Security researchers run honeypots exposed to the open internet to collect data on what attacks are currently popular, what passwords are being tried, and what exploits are circulating.
- Building one teaches you both sides at once. You have to understand what makes a service look real and tempting in order to fake it properly.

## How it actually works

1. Pick a service to impersonate, such as SSH or a basic web login form.
2. Build a fake version that accepts connections and looks functional.
   - A fake SSH server that accepts any username and password, logs the attempt, then disconnects or pretends to grant access to a fake shell.
   - A fake web login page that accepts any credentials, logs them, and shows a believable login failed message.
3. Log everything: source IP, timestamp, username, password tried, and any commands typed if you are faking a shell.
4. Never let it touch anything real. The honeypot must be fully isolated, with no real data, no real credentials, and no path back into anything that matters.
5. Analyze the data: look for patterns such as which usernames and passwords are tried most, whether the same IPs keep returning, or whether attacks spike at certain times.

## Build it yourself (core pieces)

- A fake SSH honeypot is a great starting project. Libraries like `paramiko` let you implement just enough of the SSH protocol to accept connections and log credentials without authenticating anyone.
- A fake web login is even simpler: a basic Flask app with a login form that always logs the attempt and always shows invalid credentials.
- Add fake bait: give your fake shell a few believable fake files and directories such as `config.txt` or `backup.sql` to see if attackers poke around further once they are "in."
- Consider running it on a cheap cloud VM exposed to the real internet, fully isolated and with nothing of value on it. You will be surprised how quickly random scanning bots start hitting it.

## Where to practice safely

- Run honeypots only on machines and accounts you own and keep them fully isolated from anything real.
- If you expose one to the public internet, make sure it is on a throwaway VM with zero real data, zero reused credentials, and no network path back into anything you care about.
