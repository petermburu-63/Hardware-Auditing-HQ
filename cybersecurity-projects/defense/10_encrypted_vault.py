#!/usr/bin/env python3
"""
Encrypted File Vault
-----------------------
Password-based file encryption using AES-256-GCM (authenticated
encryption) with a scrypt-derived key. Uses only audited primitives
from the `cryptography` library — never hand-rolled crypto.

Requires: cryptography   (pip install cryptography)

Usage:
    python3 10_encrypted_vault.py encrypt myfile.txt --password
    python3 10_encrypted_vault.py decrypt myfile.txt.vault --password

File format (all binary, concatenated):
    [16 bytes salt][12 bytes nonce][ciphertext + 16-byte auth tag]
"""

from __future__ import annotations

import argparse
import getpass
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
VAULT_SUFFIX = ".vault"


def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key from a password using scrypt (deliberately slow)."""
    kdf = Scrypt(salt=salt, length=KEY_SIZE, n=2**14, r=8, p=1)
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(input_path: Path, password: str, output_path: Path) -> None:
    plaintext = input_path.read_bytes()

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    output_path.write_bytes(salt + nonce + ciphertext)


def decrypt_file(input_path: Path, password: str, output_path: Path) -> None:
    blob = input_path.read_bytes()
    if len(blob) < SALT_SIZE + NONCE_SIZE:
        raise SystemExit("File is too short to be a valid vault file.")

    salt = blob[:SALT_SIZE]
    nonce = blob[SALT_SIZE : SALT_SIZE + NONCE_SIZE]
    ciphertext = blob[SALT_SIZE + NONCE_SIZE :]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)

    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except Exception as exc:  # cryptography raises InvalidTag on wrong password/tampering
        raise SystemExit(
            "Decryption failed — wrong password, or the file was corrupted/tampered with."
        ) from exc

    output_path.write_bytes(plaintext)


def main() -> None:
    parser = argparse.ArgumentParser(description="AES-256-GCM encrypted file vault.")
    parser.add_argument("action", choices=["encrypt", "decrypt"])
    parser.add_argument("file", type=Path, help="File to encrypt, or .vault file to decrypt")
    parser.add_argument("--password", action="store_true", help="Prompt for a password securely")
    parser.add_argument("--out", type=Path, help="Output path (optional)")
    args = parser.parse_args()

    if not args.file.exists():
        raise SystemExit(f"File not found: {args.file}")

    if args.password:
        password = getpass.getpass("Password: ")
        if args.action == "encrypt":
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                raise SystemExit("Passwords did not match.")
    else:
        password = getpass.getpass("Password: ")

    if args.action == "encrypt":
        output_path = args.out or args.file.with_suffix(args.file.suffix + VAULT_SUFFIX)
        encrypt_file(args.file, password, output_path)
        print(f"Encrypted -> {output_path}")
    else:
        if args.out:
            output_path = args.out
        elif args.file.name.endswith(VAULT_SUFFIX):
            output_path = args.file.with_suffix("")
        else:
            output_path = args.file.with_suffix(args.file.suffix + ".decrypted")
        decrypt_file(args.file, password, output_path)
        print(f"Decrypted -> {output_path}")


if __name__ == "__main__":
    main()
