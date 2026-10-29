# Home Lab Risk Scenario

## Scenario summary

A lab environment contains a local web service, a database, and a summary monitoring tool. The system begins to show repeated failed authentication, bursts of outbound connections, and unexpected service changes.

## What to inspect

- auth logs
- firewall rules
- running services
- startup scripts
- scheduled tasks
- service metadata and versioning

## Triage path

1. confirm the timeline
2. isolate affected endpoints
3. compare current state to baseline
4. confirm if the activity is legitimate or suspicious
5. record impact and remediation steps

## Outcome

This scenario is useful for understanding how a small environment can drift into suspicious behavior and how to reason through it without panicking.
