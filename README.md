# Hardware Auditing HQ

A security and systems research workspace for structured device reviews, telemetry analysis, and evidence-based hardening. The project is designed to make observations reproducible and to separate measured evidence from assumptions.

> **Authorized use only:** Use these materials on systems you own or are explicitly authorized to assess. Keep test data synthetic or appropriately sanitized.

## At a glance

- **Focus:** device baselines, telemetry, configuration drift, and defensive recommendations
- **Includes:** Python lab exercises, research notes, case studies, templates, and architecture documentation
- **Audience:** learners and practitioners building a careful, repeatable home-lab or internal-review workflow

## Contents

| Path | Purpose |
| --- | --- |
| [`cybersecurity-projects/`](cybersecurity-projects/) | Python exercises grouped into discovery, defense, and analytics |
| [`research-notebook/`](research-notebook/) | Baseline, investigation, and review notes |
| [`docs/`](docs/) | Project index, methodology, scenarios, and case studies |
| [`telemetry_dumps/`](telemetry_dumps/) | Example telemetry and reference material; inspect and sanitize before sharing |
| [`notes/`](notes/) | Informal observations to develop into documented findings |
| [`tools/`](tools/) | Small local project utilities |

Start with the [project index](docs/PROJECT_INDEX.md), [research methodology](docs/RESEARCH_METHODOLOGY.md), and [lab guide](cybersecurity-projects/docs/SECURITY_LAB_GUIDE.md).

## Research workflow

1. **Define scope:** Record the system, authorization, review window, and questions.
2. **Establish a baseline:** Document expected configuration and normal behavior.
3. **Collect evidence:** Capture relevant observations with timestamps and provenance.
4. **Analyze carefully:** Separate facts, hypotheses, and limitations; account for benign explanations.
5. **Recommend proportionately:** Prioritize practical, reversible hardening actions.
6. **Verify and report:** Re-check changes and summarize outcomes without exposing sensitive data.

## Set up

Requires Python 3. Create a virtual environment and install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r cybersecurity-projects/requirements.txt
```

Review the documentation and each exercise's options before use. Some exercises may require operating-system-specific permissions or dependencies. The `.env.example` file is a reference only; keep real secrets in local environment configuration and never commit them.

## Project structure

```text
.
├── cybersecurity-projects/
│   ├── analytics/       # Telemetry and risk analysis
│   ├── defense/         # Monitoring and defensive exercises
│   ├── docs/            # Architecture, guides, and scenarios
│   └── offense/         # Authorized discovery exercises
├── docs/                # Indexes, methodology, and case studies
├── notes/               # Working observations
├── research-notebook/   # Structured research entries and templates
├── telemetry_dumps/     # Example data and reference material
└── tools/               # Local project utilities
```

## Responsible research

- Work only within a clearly authorized scope.
- Prefer isolated lab systems and synthetic or sanitized data.
- Do not publish credentials, personal information, or sensitive captures.
- Document tool limitations and uncertainty alongside findings.
- Treat results as learning and review artifacts, not proof of a vulnerability without validation.

## License

See [LICENSE](LICENSE) for the applicable license terms.

## Author

Peter Mburu
