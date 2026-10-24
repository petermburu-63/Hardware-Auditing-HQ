# Project 10: Encrypted File Vault

**Side:** Defense (applied cryptography) · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

An encrypted vault takes your files and scrambles them with a key derived from a password you choose, so that without the right password, the data is unrecoverable, computationally-infeasible-to-brute-force noise. This is the same underlying idea as tools like VeraCrypt, or what happens under the hood when you password-protect a zip file — except you're going to build the real, properly-done version instead of treating it as magic.

## Why it matters

- Nearly every other project on this list is about **detecting** attacks. This one is about **preventing damage even after a breach** — if someone steals your encrypted files, they get nothing usable.
- It forces you to actually understand cryptographic concepts that get thrown around constantly but rarely explained: symmetric encryption, key derivation, salts, IVs/nonces, and authenticated encryption.
- It also teaches you, concretely, why "roll your own crypto" is a famous warning in security — there are several easy-to-make mistakes here that silently destroy your security while looking like it works perfectly.

## How it actually works

1. **Key derivation**: you can't use a human password directly as an encryption key — passwords are low-entropy and the wrong length. Instead, run the password through a **Key Derivation Function** (KDF) like PBKDF2, scrypt, or Argon2, along with a random **salt**, to produce a proper-length cryptographic key. This is deliberately slow (same idea as Project 3's hash cracking defense) so that brute-forcing the password is expensive.
2. **Encryption**: use a modern **authenticated** symmetric cipher — AES-GCM or ChaCha20-Poly1305 — never a plain, unauthenticated mode. "Authenticated" means the cipher also detects if the ciphertext was tampered with, not just that it hides the content.
3. **Nonce/IV**: every encryption operation needs a fresh, unique number (nonce/IV) so that encrypting the same data twice doesn't produce the same output — reusing a nonce with certain cipher modes can catastrophically break the encryption's security guarantees.
4. **Store together**: the salt, the nonce, and the ciphertext all need to be saved (none of them are secret on their own) — only the password/derived key is secret.
5. **Decryption**: reverse the process — derive the key from the password + stored salt, then decrypt using the stored nonce, and verify the authentication tag matches before trusting the output.

## Build it yourself (core pieces)

- Use a real, audited crypto library — in Python, the `cryptography` package (specifically `cryptography.hazmat.primitives.ciphers.aead.AESGCM`) is the trustworthy choice. **Do not** hand-write your own cipher or "obfuscation" scheme and call it encryption — that's the classic beginner mistake this project exists to steer you away from.
- Build the CLI flow: `vault.py encrypt myfile.txt --password` → produces `myfile.txt.vault` containing salt + nonce + ciphertext + auth tag.
- Build the matching `vault.py decrypt myfile.txt.vault --password` flow, and make sure it correctly *fails* (doesn't just produce garbage) when given the wrong password.
- Stretch goal: add multi-file support (encrypt a whole folder) and a "wrong password" test suite to prove your authentication check actually catches tampering and wrong passwords reliably.

## Where to practice safely

- Fully safe — this is purely defensive, applied cryptography on your own test files. There's no "target" to avoid here; the main risk is encrypting something important with a password you then forget, so test with throwaway files first.
