#!/usr/bin/env python3
"""
Password Hash Cracker (dictionary attack)
-------------------------------------------
Educational tool for cracking hashes YOU generated yourself, to learn
how wordlist attacks work and why salting + slow hashes matter.

Usage:
    # Generate a practice hash:
    python3 03_hash_cracker.py --make-hash "letmein123" --algo sha256

    # Crack it against a wordlist:
    python3 03_hash_cracker.py --crack <hash> --wordlist rockyou.txt --algo sha256

    # With a salt (format must match how you salted it: salt + password):
    python3 03_hash_cracker.py --crack <hash> --wordlist rockyou.txt --algo sha256 --salt abc123
"""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path


def hash_candidate(candidate: str, algo: str, salt: str = "") -> str:
    """Hash salt+candidate using the chosen algorithm."""
    hasher = hashlib.new(algo)
    hasher.update((salt + candidate).encode("utf-8"))
    return hasher.hexdigest()


def crack(target_hash: str, wordlist_path: Path, algo: str, salt: str = "") -> tuple[str | None, int, float]:
    """
    Try every line of `wordlist_path` against `target_hash`.
    Returns (found_password_or_None, attempts_made, seconds_elapsed).
    """
    target_hash = target_hash.lower().strip()
    start = time.time()
    attempts = 0

    with wordlist_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            candidate = line.rstrip("\n").rstrip("\r")
            if not candidate:
                continue
            attempts += 1
            if hash_candidate(candidate, algo, salt) == target_hash:
                return candidate, attempts, time.time() - start

    return None, attempts, time.time() - start


def main() -> None:
    parser = argparse.ArgumentParser(description="Dictionary-attack hash cracker (practice use only).")
    parser.add_argument("--algo", default="sha256", choices=sorted(hashlib.algorithms_guaranteed))
    parser.add_argument("--salt", default="", help="Salt prepended before hashing (if any)")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--make-hash", metavar="PASSWORD", help="Generate a hash from a password (for testing)")
    mode.add_argument("--crack", metavar="HASH", help="The target hash to crack")

    parser.add_argument("--wordlist", type=Path, help="Path to a wordlist file (required with --crack)")
    args = parser.parse_args()

    if args.make_hash is not None:
        digest = hash_candidate(args.make_hash, args.algo, args.salt)
        print(f"{args.algo}(salt + password) = {digest}")
        return

    if not args.wordlist:
        parser.error("--wordlist is required when using --crack")
    if not args.wordlist.exists():
        parser.error(f"Wordlist not found: {args.wordlist}")

    print(f"Cracking with {args.algo}, wordlist={args.wordlist} ...")
    found, attempts, elapsed = crack(args.crack, args.wordlist, args.algo, args.salt)

    if found is not None:
        print(f"MATCH FOUND: '{found}'  (after {attempts} attempts, {elapsed:.2f}s)")
    else:
        print(f"No match in wordlist ({attempts} attempts, {elapsed:.2f}s)")


if __name__ == "__main__":
    main()
