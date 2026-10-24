# Project 3: Password Hash Cracker

**Side:** Offense · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

Websites and systems don't store your actual password — they store a **hash** of it, which is the output of a one-way mathematical function. "password123" might become something like `ef92b778...`. You can turn a password into its hash easily, but you (in theory) can't turn the hash back into the password. So when a site's database leaks, attackers don't get your plaintext password — they get a pile of hashes, and have to *guess* which plaintext produces each hash.

A **hash cracker** automates that guessing. You feed it a list of hashes and a list of candidate passwords (a "wordlist"), and it hashes every candidate and checks for a match.

## Why it matters

- This is literally how security researchers (and attackers) test password strength after a breach — tools like **Hashcat** and **John the Ripper** are industry-standard versions of what you're building.
- Understanding this is *why* "password123" is terrible (it's in every wordlist on earth and cracks in milliseconds) and why long, random, unique passwords matter (they're not in any wordlist, and brute-forcing them would take longer than the universe has existed).
- It teaches you directly why companies are moving to **salting** (adding random data to each password before hashing, so the same password doesn't produce the same hash twice) and slow hash functions like bcrypt/scrypt/Argon2 (designed to make this exact attack painfully slow).

## How it actually works

1. **Dictionary attack**: take a wordlist (millions of real leaked passwords, like the famous `rockyou.txt`), hash each one, and compare it to your target hash. If it matches, you've found the password.
2. **Brute-force attack**: instead of a wordlist, generate every possible combination of characters up to a certain length. Exhaustive, but only realistic for short/simple passwords — the combinations explode exponentially with length.
3. **Rule-based attacks**: take wordlist entries and apply common human tweaks (capitalize first letter, add "123" or "!" at the end, replace "a" with "@") since people modify dictionary words in predictable ways rather than picking random passwords.
4. **Salted hashes**: if the target system added a random "salt" before hashing, you need to know the salt (it's usually stored alongside the hash, not secret) and include it in every guess.

## Build it yourself (core pieces)

- Python's built-in `hashlib` gives you MD5, SHA-1, SHA-256, etc.
- Start with: given one hash and one wordlist file, find the matching line.
- Add salting support: hash `salt + password` instead of just `password`, and test against a database of salted hashes you generate yourself.
- Measure and compare: time how long MD5 cracking takes vs. bcrypt cracking for the same wordlist — this single comparison teaches the whole point of slow hash functions better than any article will.

## Where to practice safely

- **Only crack hashes you created yourself** from passwords you made up for this project, or hashes explicitly provided for practice (CTF challenges, Hack The Box/TryHackMe exercises).
- Never run this against real leaked credential databases tied to real people, and never target anyone else's accounts — that crosses from "learning" into unauthorized access, which is illegal.
