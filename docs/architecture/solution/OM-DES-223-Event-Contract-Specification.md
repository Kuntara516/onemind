# OM-DES-223

# Event Contract Specification

**Document ID:** OM-DES-223

**Document Title:** Event Contract Specification

**Domain:** Solution Design

**Version:** 1.0

**Status:** Draft

**Owner:** OneMind Architecture Team

**Classification:** Internal

---

# 1. Purpose

This document defines the engineering standards for event contracts used throughout the OneMind Enterprise AI Operating Platform.

Event Contracts provide a consistent, versioned, and reliable mechanism for asynchronous communication between services, workflows, AI agents, integrations, and external systems.

This specification applies to every event published or consumed within the OneMind platform.

---

# 2. References

This specification shall be read together with:

* OM-DES-220 — API Design Standards
* OM-DES-221 — REST API Specification
* OM-DES-222 — MCP Tool Specification
* OM-DES-216 — Integration Domain Design

---

# 3. Design Objectives

Event contracts shall be:

* Consistent
* Immutable
* Versioned
* Traceable
* Self-describing
* Backward Compatible
* Observable
* Technology Independent

---

# 4. Event-Driven Architecture

```text
Producer
    │
    ▼
 Event Publisher
    │
──────── Event Bus ────────
    │
    ├────────► Workflow Engine
    │
    ├────────► AI Agents
    │
    ├────────► Integration Services
    │
    ├────────► Notification Service
    │
    └────────► Analytics Platform
```

Events shall be published once and consumed by one or more subscribers.

---

# 5. Event Naming Convention

Event names shall follow:

```text
<Domain>.<Entity>.<Action>
```

Examples

```text
Identity.User.Created

Identity.User.Disabled

Workflow.Execution.Started

Workflow.Execution.Completed

Knowledge.Document.Indexed

Memory.Session.Created

Agent.Task.Assigned

Agent.Task.Completed

Integration.Sync.Completed

Notification.Email.Sent
```

Use PascalCase for every segment.

---

# 6. Event Envelope

Every event shall contain a common envelope.

Example

```json
{
  "eventId": "5f3d6d5a-a2db-49db-a79f-5f3cba847b42",
  "eventType": "Workflow.Execution.Completed",
  "eventVersion": "1.0",
  "occurredAt": "2026-07-14T12:00:00Z",
  "tenantId": "tenant-001",
  "correlationId": "ab23cd45",
  "source": "workflow-service",
  "data": {}
}
```

---

# 7. Mandatory Fields

Every event shall include:

| Field         | Description                  |
| ------------- | ---------------------------- |
| eventId       | UUID                         |
| eventType     | Event name                   |
| eventVersion  | Schema version               |
| occurredAt    | ISO-8601 UTC timestamp       |
| source        | Publishing service           |
| correlationId | Distributed trace identifier |
| tenantId      | Multi-tenant context         |
| data          | Business payload             |

---

# 8. Event Payload

Business data shall reside only within the **data** object.

Example

```json
{
  "data": {
    "workflowId": "wf-1001",
    "status": "Completed",
    "duration": 42
  }
}
```

Payloads shall avoid implementation-specific details.

---

# 9. Event Schema

Every event shall have a published JSON Schema.

Representative structure

```text
schemas/events/

Identity.User.Created.json

Workflow.Execution.Completed.json

Knowledge.Document.Indexed.json
```

Schema validation shall occur before publishing.

---

# 10. Event Versioning

Semantic Versioning shall be used.

| Version | Meaning             |
| ------- | ------------------- |
| 1.x     | Backward compatible |
| 2.x     | Breaking change     |

Breaking changes require a new major version.

---

# 11. Event Ordering

Where ordering is required:

* Preserve ordering per aggregate.
* Do not assume global ordering.
* Consumers shall tolerate duplicate events.

---

# 12. Delivery Semantics

The platform shall support:

* At Least Once Delivery
* Retry Policies
* Dead Letter Queue (DLQ)
* Poison Message Handling

Consumers shall be idempotent.

---

# 13. Event Lifecycle

```text
Created
    │
    ▼
Validated
    │
    ▼
Published
    │
    ▼
Consumed
    │
    ▼
Processed
    │
    ▼
Archived
```

---

# 14. Error Handling

Failures during event processing shall:

* Retry according to policy
* Record structured logs
* Emit metrics
* Preserve correlation IDs
* Route failed messages to the DLQ when retry limits are exceeded

---

# 15. Security Requirements

Events shall implement:

* TLS encryption in transit
* Payload validation
* Sensitive data masking
* Digital integrity verification (where required)
* Authorization for publishers and subscribers

Personally identifiable information (PII) shall only be included when justified and protected according to organizational privacy policies.

---

# 16. Observability

Every event shall generate:

* Structured logs
* Metrics
* Distributed traces
* Audit records

Representative metrics:

* Published Events
* Failed Publications
* Consumer Latency
* Retry Count
* DLQ Count

---

# 17. Event Registry

All event definitions shall be maintained in a centralized Event Registry.

Each registered event shall include:

* Name
* Description
* Owner
* Schema
* Version
* Producer
* Consumers
* Status

---

# 18. Reference Implementation

```text
events/
├── schemas/
├── registry/
├── producers/
├── consumers/
├── validation/
└── tests/
```

---

# 19. Event Design Checklist

Before publishing an event:

* Event name follows standard
* Envelope complete
* Schema validated
* Payload minimized
* Version assigned
* Documentation published
* Observability enabled
* Security reviewed
* Consumers identified
* Registry updated

---

# 20. Related Documents

Architecture

* OM-SOL-121 — Enterprise Integration Architecture
* OM-SOL-123 — Observability Architecture

Design

* OM-DES-216 — Integration Domain Design
* OM-DES-220 — API Design Standards
* OM-DES-221 — REST API Specification
* OM-DES-222 — MCP Tool Specification
* OM-DES-224 — Webhook & Callback Specification

---

# 21. Summary

This specification establishes a unified standard for event contracts across the OneMind platform.

By standardizing event naming, envelopes, schemas, versioning, lifecycle, security, and observability, OneMind enables reliable, scalable, and loosely coupled event-driven communication between AI agents, workflows, enterprise services, and external systems.

---

**End of Document**

**Document ID:** OM-DES-223

**Version:** 1.0

**Status:** Draft

**Milestone:** M5 – Solution Design

**Many Agents. One Mind.**
