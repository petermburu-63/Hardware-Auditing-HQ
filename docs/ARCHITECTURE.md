# Architecture Overview

```mermaid
flowchart TD
    A[Target System or Lab Environment] --> B[Discovery & Service Review]
    B --> C[Telemetry & Log Collection]
    B --> D[System Baseline Review]
    C --> E[Pattern Detection & Risk Analysis]
    D --> E
    E --> F[Operational Findings]
    F --> G[Hardening Recommendations]
    G --> H[Verification and Follow-up]
```

## Core layers

### 1. Discovery layer
This layer focuses on what is visible to the outside world: open ports, exposed services, service banners, and initial host posture.

### 2. Telemetry layer
This layer captures the operational and log-based signals that help explain what is happening inside the system or environment.

### 3. Defensive layer
This layer monitors ongoing drift, integrity changes, and suspicious events. It represents the monitoring side of a practical security workflow.

### 4. Analytics layer
This layer converts observations into summaries and risk patterns that are easier to understand and act on.

### 5. Evidence and reporting layer
This layer turns the raw signal into written findings, recommendations, and research notes.

## Design philosophy

The architecture is intentionally modular. A good lab or research repo should make it easy to reason about each stage without mixing discovery, detection, and reporting into one giant script.
