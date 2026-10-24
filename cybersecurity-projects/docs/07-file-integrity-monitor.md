# Project 7: File Integrity Monitor (FIM)

**Side:** Defense · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

A file integrity monitor watches important files on a system and alerts you the instant one of them changes unexpectedly. The trick is that it does not need to understand why a file changed. It only needs to reliably notice that it changed. It uses the same hash concept as Project 3: a file's hash is like its fingerprint, and if even one character inside it changes, the fingerprint changes completely.

## Why it matters

- This is one of the most reliable, low-noise ways to catch an intrusion.
- If an attacker modifies a system file, plants a backdoor in a config, or replaces a legitimate program with a malicious one, a FIM catches it even if every other defense failed.
- It is required by major compliance standards because it is such an effective, simple control.
- It is one of the easier defensive tools to build well, which makes it a great confidence-building project before tackling bigger ones.

## How it actually works

1. Baseline: pick a set of files or directories that matter and compute a cryptographic hash for each one. Store these hashes somewhere safe, ideally not on the same machine so an attacker cannot simply edit the baseline to hide their tracks.
2. Re-check on a schedule: periodically recompute the hash of each watched file.
3. Compare: if a file's current hash does not match its baseline hash, something changed. Flag it.
4. Classify the change: was the file modified, deleted, or did its permissions change? Each matters differently.
5. Alert: log it, email it, or feed it into a larger system such as the HIDS from Project 4.

## Build it yourself (core pieces)

- `hashlib.sha256()` on file contents is all the core logic needs.
- Store your baseline as a simple JSON file such as `/etc/passwd` to a hash string.
- For efficiency on large file sets, use native file-change notifications instead of constantly rehashing everything. On Linux, this is `inotify`.
- Track metadata such as size, permissions, owner, and last modified time alongside the hash. Sometimes metadata changes are suspicious even before the content changes.
- Stretch goal: store baseline hashes signed with a private key so an attacker cannot silently edit the baseline file to cover their tracks.

## Where to practice safely

- Entirely safe to build and test on your own machine or VM.
- To test it properly, deliberately modify a protected test file yourself and confirm your tool catches it, then delete one and confirm that is caught too.
