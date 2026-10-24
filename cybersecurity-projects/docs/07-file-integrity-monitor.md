# Project 7: File Integrity Monitor (FIM)

**Side:** Defense · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

A **File Integrity Monitor** watches important files on a system and alerts you the instant one of them changes unexpectedly. The trick is that it doesn't need to understand *why* a file changed to be useful — it just needs to reliably notice *that* it changed, using the same "hash" concept from Project 3: a file's hash is like its fingerprint, and if even one character inside it changes, the fingerprint changes completely.

## Why it matters

- This is one of the most reliable, low-noise ways to catch an intrusion. If an attacker modifies a system file, plants a backdoor in a config, or replaces a legitimate program with a malicious one, a FIM catches it even if every other defense failed.
- It's required by major compliance standards (PCI-DSS for anyone handling credit card data, for example) specifically because it's such an effective, simple control.
- It's genuinely one of the easier defensive tools to build well, which makes it a great confidence-building project before tackling something like Project 4 or 9.

## How it actually works

1. **Baseline**: pick a set of files/directories that matter (system binaries, config files, a web app's source code) and compute a cryptographic hash (SHA-256 is the standard choice) of each one. Store these hashes somewhere safe — ideally not on the same machine, so an attacker can't just edit the baseline to hide their tracks.
2. **Re-check on a schedule**: periodically (every few minutes, or on every file-system event) recompute the hash of each watched file.
3. **Compare**: if a file's current hash doesn't match its baseline hash, something changed. Flag it.
4. **Classify the change**: was the file modified, deleted, or did its permissions change? Each matters differently — a permissions change on `/etc/shadow` (the password file on Linux) is a huge red flag even if the content didn't change.
5. **Alert**: log it, email it, or feed it into a bigger system like the HIDS from Project 4.

## Build it yourself (core pieces)

- `hashlib.sha256()` on file contents is all the core logic needs.
- Store your baseline as a simple JSON file: `{"/etc/passwd": "a1b2c3...", "/bin/ls": "d4e5f6..."}`.
- For efficiency on large file sets, use the OS's native file-change notifications instead of constantly re-hashing everything — on Linux this is `inotify` (Python: the `watchdog` library wraps it nicely), which tells you instantly when a file changes instead of you having to poll.
- Also track file **metadata** (size, permissions, owner, last-modified time) alongside the hash — sometimes the metadata changing is itself suspicious even before you re-hash.
- Stretch goal: store your baseline hashes signed with a private key, so even if an attacker gets admin access, they can't quietly edit the baseline file to cover their tracks without invalidating the signature.

## Where to practice safely

- Entirely safe to build and test on your own machine or VM — you're only reading and hashing files you own.
- To test it properly, deliberately modify a "protected" test file yourself and confirm your tool catches it, then try deleting one and confirm that's caught too.
