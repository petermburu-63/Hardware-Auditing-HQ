# Advanced Lab Scenarios

## Scenario 1: home lab drift

A small internal system starts to show odd service exposure, unexpected background activity, and repeated failed logins. The review should focus on:

- port exposure
- service versions and banners
- auth logs
- startup services
- firewall behavior
- software baselines

## Scenario 2: stale machine review

A machine that was previously stable begins to behave differently after a software update. The investigation should examine:

- changes in services or enabled startup tasks
- log anomalies
- new listening ports
- telemetry behaviors
- recent package changes

## Scenario 3: telemetry noise vs risk

A system generates lots of warnings that may not be dangerous by themselves. The task is to determine whether the warnings are benign, part of a pattern, or evidence of escalating drift.

## Scenario 4: edge device security posture

A low-cost device or embedded endpoint exposes a surprisingly broad surface area. The project review should assess:

- what is exposed by default
- which services are truly needed
- what is being collected or transmitted
- how much telemetry is unnecessary

## Scenario 5: hardening after evidence

After reviewing logs and telemetry, a package of changes is proposed. The outcome should be measured after deployment to determine whether risk reduced, drift flattened, or new issues became visible.
