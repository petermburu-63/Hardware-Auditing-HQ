# Telemetry Log Review: Assignment Summary

## Overview
This repository contains a set of telemetry dump logs that reflect a realistic chain of system events. Together, they show how one small issue can trigger larger failures across a server environment.

## What the logs show
The logs cover five main events:

1. SSH brute-force attempts
   - An external IP repeatedly tried common usernames such as root, admin, and support.
   - The system detected this pattern and blocked the traffic using Fail2Ban and UFW.
   - This is a common attack method known as password guessing or brute-force login attempts.

2. Web server rate limiting
   - NGINX began limiting requests from a suspicious client.
   - The upstream application encountered errors and started returning 503 responses.
   - This suggests the web layer was still protecting itself, but the backend service was unhealthy.

3. Memory exhaustion in Docker
   - A Node.js process was killed by the Linux kernel due to memory pressure.
   - The container exit code was 137, which is consistent with an OOM kill.
   - This shows resource exhaustion in a containerized environment.

4. PostgreSQL overload and SYN flood pattern
   - PostgreSQL hit its maximum connection limit.
   - The database rejected new clients because all connection slots were taken.
   - A SYN flood warning indicates an attempted denial-of-service event against the database port.

5. The “quantum panic” file
   - This is intentionally exaggerated and comedic.
   - It is not real telemetry in the same way as the others.
   - It is included as a satirical log to make the repo memorable and to show the difference between serious evidence and stylized fiction.

## Why the logs matter
These logs are useful for learning because they show how multiple systems are linked:
- SSH security
- web protection
- backend reliability
- database capacity
- resource control
- attack detection and response

When one part fails, the rest of the system may also fail. This is a common real-world problem in cyber operations and infrastructure security.

## Key cybersecurity lessons
- Attack attempts are common and should be expected.
- Security tools like fail2ban and firewalls help reduce risk.
- Rate limiting protects systems from overload.
- OOM kills are serious signs of memory pressure.
- Databases can become unavailable when overrun with connections.
- Logs are essential for detecting malicious activity and diagnosing system failures.

## Conclusion
The logs are strong educational material for a first-year cyber security student because they combine practical examples of:
- attack detection,
- service degradation,
- system resource failure,
- and incident response patterns.

They are especially useful because they demonstrate both defensive security and operational resilience in a format that is easy to reason about.
