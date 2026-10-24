#!/usr/bin/env python3
"""
Fake SSH Honeypot
-------------------
Accepts SSH connections, logs whatever username/password is tried,
and always rejects authentication (nothing real to protect, nothing
real to steal). Run this only on an isolated lab VM with no real data
or credentials anywhere on it.

Requires: paramiko   (pip install paramiko)
Requires a host key — generate one once with:
    ssh-keygen -t rsa -b 2048 -f honeypot_host_key -N ""

Usage:
    python3 05_honeypot.py --host 0.0.0.0 --port 2222 --hostkey honeypot_host_key
"""

from __future__ import annotations

import argparse
import json
import socket
import threading
from datetime import datetime, timezone
from pathlib import Path

try:
    import paramiko  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("This script requires paramiko: pip install paramiko") from exc


def log_event(log_path: Path, event: dict) -> None:
    event["timestamp"] = datetime.now(timezone.utc).isoformat()
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
    print(f"[LOG] {event}")


class HoneypotServer(paramiko.ServerInterface):
    """Always logs credentials, always denies auth."""

    def __init__(self, client_ip: str, log_path: Path) -> None:
        super().__init__()
        self.client_ip = client_ip
        self.log_path = log_path
        self.event = threading.Event()

    def check_auth_password(self, username: str, password: str) -> int:
        log_event(self.log_path, {
            "event": "login_attempt",
            "src_ip": self.client_ip,
            "username": username,
            "password": password,
        })
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username: str, key) -> int:
        log_event(self.log_path, {
            "event": "pubkey_attempt",
            "src_ip": self.client_ip,
            "username": username,
            "key_fingerprint": key.get_fingerprint().hex(),
        })
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username: str) -> str:
        return "password,publickey"

    def check_channel_request(self, kind: str, chanid: int) -> int:
        return paramiko.OPEN_SUCCEEDED if kind == "session" else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


def handle_connection(client_sock: socket.socket, client_addr, host_key, log_path: Path) -> None:
    client_ip = client_addr[0]
    transport = paramiko.Transport(client_sock)
    transport.add_server_key(host_key)
    server = HoneypotServer(client_ip, log_path)

    try:
        transport.start_server(server=server)
        channel = transport.accept(timeout=10)
        if channel is not None:
            channel.close()
    except Exception as exc:  # noqa: BLE001 - honeypots must never crash on bad input
        log_event(log_path, {"event": "error", "src_ip": client_ip, "detail": str(exc)})
    finally:
        transport.close()
        log_event(log_path, {"event": "disconnect", "src_ip": client_ip})


def main() -> None:
    parser = argparse.ArgumentParser(description="Fake SSH honeypot that logs login attempts.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=2222)
    parser.add_argument("--hostkey", type=Path, required=True, help="Path to an RSA host key file")
    parser.add_argument("--log", type=Path, default=Path("honeypot_log.jsonl"))
    args = parser.parse_args()

    if not args.hostkey.exists():
        raise SystemExit(
            f"Host key not found: {args.hostkey}\n"
            f"Generate one with: ssh-keygen -t rsa -b 2048 -f {args.hostkey} -N ''"
        )

    host_key = paramiko.RSAKey.from_private_key_file(str(args.hostkey))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.host, args.port))
    sock.listen(100)

    print(f"Honeypot listening on {args.host}:{args.port} — logging to {args.log}")

    try:
        while True:
            client_sock, client_addr = sock.accept()
            log_event(args.log, {"event": "connection", "src_ip": client_addr[0]})
            thread = threading.Thread(
                target=handle_connection,
                args=(client_sock, client_addr, host_key, args.log),
                daemon=True,
            )
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
