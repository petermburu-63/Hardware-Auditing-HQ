# Telemetry Log Glossary

## Basic Terms

### Log
A log is a record of events written by a system. It is like a timeline of what happened.

### Telemetry
Telemetry means system-generated data used to monitor performance, security, and health.

### Incident
An incident is any event that disrupts normal operation or creates possible security risk.

### Brute-force attack
An attack where an attacker repeatedly tries guesses to break into a system.

### Fail2Ban
A tool that detects repeated failed login attempts and blocks the attacking IP address.

### UFW
Uncomplicated Firewall. A simple Linux firewall used to block traffic.

### NGINX
A web server and reverse proxy used to route traffic between users and application servers.

### Rate limiting
A method used to control how many requests a user or service can make in a given time.

### HTTP 503
A status code meaning the server is temporarily unavailable.

### OOM kill
Out-of-memory kill. The kernel terminates a process because it used too much RAM.

### Docker / Container
A lightweight way to run apps in isolated environments.

### cgroup v2
Linux resource management used by modern systems to control CPU, memory, and other resources.

### PostgreSQL
A popular relational database management system.

### Max connections
The maximum number of simultaneous database connections allowed.

### SYN flood
A denial-of-service method that sends a large number of connection requests to overwhelm a server.

### Kernel
The core part of the operating system that manages hardware and process scheduling.

### Upstream
The service behind a web server or proxy that the server forwards traffic to.

### Connection refused
The program or service is not accepting any new connections.

### Denial-of-service (DoS)
An attack designed to make a system unavailable.

### Cascade failure
When one bad event triggers more failures across the system.

---

## Security-Focused Terms

### Attack surface
The parts of a system that could be exposed to attackers.

### Authentication
The process of proving identity before allowing access.

### Authorization
The rules that define what an authenticated user is allowed to do.

### Vulnerability
A weakness in software, configuration, or hardware that can be exploited.

### Exploit
A technique or tool used to take advantage of a vulnerability.

### Monitoring
The practice of collecting and reviewing system data to detect issues early.

### Incident response
The process of identifying, containing, and solving a security problem.

### Resilience
The ability of a system to continue working, even when parts fail.

---

## Quick Examples
- `Invalid user root` = someone tried a bad username
- `OOMKilled: true` = the system killed a process for using too much memory
- `too many clients already` = database is full
- `RATE_LIMITED` = server refused extra traffic
- `SYN flooding` = connection flood attack

---

## Study Tip
If you see a log line and you do not know the term, ask:
- What is the system trying to do?
- What failed?
- Was it a security event or a system issue?
- Did the protection work or did the service still crash?

This helps turn raw log lines into meaningful findings.
