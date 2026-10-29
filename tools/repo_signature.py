#!/usr/bin/env python3
"""repo_signature.py

A tiny local provenance helper designed to stamp research notes and generated
artifacts with a harmless repo-origin banner.

This is intentionally lightweight and non-destructive. It is meant to help lab
work stay traceable without ruining the workflow.
"""

from __future__ import annotations

import argparse
from pathlib import Path

BANNER = """# ------------------------------------------------------------------
# Hardware Audit HQ Lab Record
# Origin: Hardware Audit HQ research environment
# Signature: GITGOOD / Hardware Audit HQ
# ------------------------------------------------------------------
"""


def add_signature(path: Path, label: str | None = None) -> None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    banner_with_label = BANNER.rstrip("\n") + f"\n# Label: {label or 'internal-lab-record'}\n"
    if raw.startswith("# ------------------------------------------------------------------"):
        return
    path.write_text(f"{banner_with_label}\n{raw}", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a harmless provenance watermark banner to a local lab artifact.")
    parser.add_argument("--path", required=True, type=Path, help="File to stamp")
    parser.add_argument("--label", default="hardware-audit-hq", help="Optional label for the artifact")
    args = parser.parse_args()

    if not args.path.exists():
        raise SystemExit(f"File does not exist: {args.path}")

    add_signature(args.path, args.label)
    print(f"Stamped {args.path} with Hardware Audit HQ provenance banner.")


if __name__ == "__main__":
    main()
