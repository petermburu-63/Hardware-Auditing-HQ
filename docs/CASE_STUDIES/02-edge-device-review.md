# Case Study 2: Edge Device Review

## Scenario
A low-cost edge or consumer device in a lab environment exposes a wider-than-expected service surface and transmits a surprising amount of telemetry data.

## Questions asked
- Which services are really required?
- Which services are leftover from an earlier configuration?
- What is the device transmitting by default?
- Which settings are noisy, unnecessary, or risky?

## Findings
- several services were enabled without a clear use case
- one network service had an outdated or unnecessary listener
- telemetry logs revealed repeated background activity during idle periods
- the device drifted from a safer baseline and was not actively monitored

## Response
The project framework suggests:

- confirm the minimum required service set
- evaluate whether telemetry is necessary
- reduce unnecessary exposure
- document the revised baseline and compare again

## Why it matters
This kind of review demonstrates how small systems can accumulate unnecessary risk over time and why baseline reviews matter.
