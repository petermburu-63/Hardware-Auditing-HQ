# Case Study 1: Home Lab Incident Review

## Scenario
A home-lab machine begins to show repeated failed login attempts, unexpected port activity, and a curious change in background service behavior.

## What was reviewed
- auth logs
- running services
- listening ports
- startup scripts
- recent config or package drift
- telemetry history

## Findings
- the pattern was not random; it was clustered in time
- a service was unexpectedly opened and had not been part of the baseline
- a small number of failed logins were associated with repeated connection bursts
- the behavior was not severe enough to be a full compromise, but it was definitely enough to justify investigation

## Impact
The most important finding was not the single alert itself. It was the fact that multiple weak signals combined into a coherent pattern.

## Recommended actions
- reset or review service configuration
- remove unneeded listening ports
- compare the service baseline against known-good state
- tighten authentication and log retention review
- repeat monitoring after cleanup

## Learning value
This is a useful example because it shows the difference between a noisy event and a real operational pattern.
