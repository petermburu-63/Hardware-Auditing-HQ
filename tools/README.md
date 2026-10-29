# Tools

This directory contains the small utility scripts used to keep the lab organized, traceable, and easier to manage locally.

## Included tooling

- `repo_signature.py` — adds a harmless provenance banner to generated lab artifacts
- `README.md` — local usage and intent notes

## Why these tools exist

The goal is not to sabotage other people or create a fake intimidation layer. It is to keep local project artifacts traceable so that the work clearly remains tied to this repo and its author, especially in a lab environment or research workflow.

## Example usage

```bash
python3 tools/repo_signature.py --path ./notes/example-report.txt --label "hardware-audit-hq"
```

This will add a header such as:

```text
# Hardware Audit HQ Lab Record
# Origin: Hardware Audit HQ research environment
# Signature: GITGOOD / Hardware Audit HQ
```
