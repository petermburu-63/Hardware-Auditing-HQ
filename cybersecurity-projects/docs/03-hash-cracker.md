# Project 3: Password Hash Cracker

**Side:** Offense · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

Websites and systems do not store your actual password. They store a hash of it, which is the output of a one-way mathematical function. "password123" might become something like `ef92b778...`. You can turn a password into a hash easily, but in theory you cannot turn the hash back into the password. So when a site's database leaks, attackers do not get your plaintext password. They get a pile of hashes and have to guess which plaintext produces each hash.

A hash cracker automates that guessing. You feed it a list of hashes and a list of candidate passwords, called a wordlist, and it hashes every candidate and checks for a match.

## Why it matters

- This is literally how security researchers and attackers test password strength after a breach. Tools like Hashcat and John the Ripper are industry-standard versions of what you are building.
- It explains why "password123" is terrible. It is in almost every wordlist and cracks in milliseconds.
- It also teaches why salting matters and why slow hash functions like bcrypt, scrypt, and Argon2 exist. They are designed to make this exact attack painfully slow.

## How it actually works

1. Dictionary attack: take a wordlist, such as millions of real leaked passwords, hash each one, and compare it to your target hash. If it matches, you have found the password.
2. Brute-force attack: instead of a wordlist, generate every possible combination of characters up to a certain length. It is exhaustive, but realistic only for short or simple passwords.
3. Rule-based attacks: take wordlist entries and apply common human tweaks, such as capitalizing the first letter, adding "123" or "!", or replacing "a" with "@". People modify dictionary words in predictable ways.
4. Salted hashes: if the target system added a random salt before hashing, you need to know the salt and include it in every guess. The salt is usually stored alongside the hash.

## Build it yourself (core pieces)

- Python's built-in `hashlib` gives you MD5, SHA-1, SHA-256, and others.
- Start with this: given one hash and one wordlist file, find the matching line.
- Add salting support: hash `salt + password` instead of just `password`, and test against a database of salted hashes you generate yourself.
- Measure and compare: time how long MD5 cracking takes versus bcrypt cracking for the same wordlist. That compares the whole point of slow hash functions better than any article will.

## Where to practice safely

- Only crack hashes you created yourself from passwords you made up for this project, or hashes explicitly provided for practice.
- Never run this against real leaked credential databases tied to real people, and never target anyone else's accounts. That crosses from learning into unauthorized access, which is illegal.
