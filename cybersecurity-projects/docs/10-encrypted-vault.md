# Project 10: Encrypted File Vault

**Side:** Defense (applied cryptography) · **Difficulty:** Mid · **Language:** Python

## What is this, in plain English?

An encrypted vault takes your files and scrambles them with a key derived from a password you choose so that without the right password, the data is unrecoverable noise. This is the same basic idea used by tools like VeraCrypt or password-protected ZIP files, except you are building the real version instead of treating it as magic.

## Why it matters

- Nearly every other project on this list is about detecting attacks. This one is about preventing damage even after a breach.
- It forces you to understand cryptographic concepts that get thrown around constantly but rarely explained: symmetric encryption, key derivation, salts, IVs and nonces, and authenticated encryption.
- It also teaches why "roll your own crypto" is such a famous warning in security.

## How it actually works

1. Key derivation: you cannot use a human password directly as an encryption key. Passwords are low entropy and the wrong length. Instead, run the password through a key derivation function such as scrypt or Argon2 with a random salt to produce a proper-length key.
2. Encryption: use a modern authenticated symmetric cipher such as AES-GCM or ChaCha20-Poly1305. Authenticated means the cipher also detects if the ciphertext was tampered with.
3. Nonce or IV: every encryption operation needs a fresh, unique number so encrypting the same data twice does not produce the same output.
4. Store together: the salt, nonce, and ciphertext all need to be saved. None of them are secret on their own; only the password or derived key is secret.
5. Decryption: reverse the process, derive the key from the password and stored salt, then decrypt and verify the authentication tag before trusting the output.

## Build it yourself (core pieces)

- Use a real, audited crypto library such as `cryptography` and `AESGCM`.
- Build the CLI flow: `encrypt myfile.txt --password` produces `myfile.txt.vault` containing salt, nonce, ciphertext, and auth tag.
- Build the matching `decrypt myfile.txt.vault --password` flow and make sure it fails correctly when given the wrong password.
- Stretch goal: add multi-file support and a wrong-password test suite.

## Where to practice safely

- Fully safe, as long as you test on throwaway files only.
- The main risk is encrypting something important with a password you then forget. Use test files first.
