# Telemetry Logs: Class Slide Summary

## Slide 1: What are telemetry logs?
Telemetry logs are records of what happened inside a system.
They capture:
- login attempts
- failed connections
- service errors
- memory use
- database connection issues
- system crashes

They are like a server's security camera footage.

---

## Slide 2: The first issue - SSH brute-force attack
The system saw repeated failed login attempts from an external IP address.
These attempts used usernames like root, admin, and support.
The system responded by blocking that IP.

Lesson: attackers often try common usernames and default passwords.

---

## Slide 3: The second issue - NGINX rate limiting
A web client triggered the NGINX request limiter.
This prevented the server from being flooded with requests.
The app then returned 503 errors because the upstream service was unhealthy.

Lesson: protective controls can prevent a crash, but they do not fix the root cause.

---

## Slide 4: The third issue - Memory exhaustion
The Node.js process in Docker was killed by the kernel because it used too much memory.
This is called an OOM kill.

Lesson: memory leaks and poor resource management can crash services.

---

## Slide 5: The fourth issue - Database overload
PostgreSQL reached its max connection count.
The system showed "too many clients already."
There was also a SYN flood warning, which suggests a denial-of-service or connection flood.

Lesson: databases are critical and can be overloaded quickly.

---

## Slide 6: Why this matters
These logs show how cyber attacks and system failures can interact.
A small attack can turn into:
- service instability,
- resource exhaustion,
- database failure,
- and widespread outages.

This is called a cascade failure.

---

## Slide 7: The funny one - Quantum log
The final log is exaggerated and intentionally fictional.
It contains absurd lines like:
- CSS parser errors in the kernel
- a toothbrush used as swap memory
- a stuck Caps Lock key in quantum superposition

This is not real telemetry. It is a humorous signal that shows the difference between a serious log and a parody.

---

## Slide 8: Final takeaway
Good cyber security professionals read logs carefully.
They ask:
- What happened?
- What system failed?
- Was it an attack, a resource issue, or both?
- What protection worked?
- What needs to be fixed?

The key skill is pattern recognition and investigation.
