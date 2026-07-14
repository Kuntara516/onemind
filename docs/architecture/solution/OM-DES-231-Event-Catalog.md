# OM-DES-231

# Event Catalog

**Document ID:** OM-DES-231

**Document Title:** Event Catalog

**Domain:** Solution Design

**Version:** 1.0

**Status:** Draft

**Owner:** OneMind Architecture Team

**Classification:** Internal

---

# 1. Purpose

This document defines the Enterprise Event Catalog for the OneMind Enterprise AI Operating Platform.

The Event Catalog provides a centralized inventory of business events used throughout the platform. It establishes common event definitions, ownership, lifecycle, and governance to ensure interoperability between services, AI agents, workflows, integrations, and external systems.

This catalog complements **OM-DES-223 Event Contract Specification** by documenting *what* events exist, while OM-DES-223 defines *how* events are structured.

---

# 2. Scope

The Event Catalog applies to:

* Business Domains
* AI Agents
* Workflow Engine
* Integration Platform
* Knowledge Platform
* Memory Platform
* Identity Services
* Notification Services
* External Integrations

---

# 3. Event Governance Principles

Every event shall:

* Represent a business fact
* Be immutable
* Have a defined owner
* Have a published schema
* Be versioned
* Be documented
* Be registered before production use

---

# 4. Event Classification

Events are grouped into domains.

| Domain       | Description                  |
| ------------ | ---------------------------- |
| Identity     | Users, Roles, Authentication |
| Tenant       | Organizations                |
| Agent        | AI Agents                    |
| Workflow     | Workflow Engine              |
| Knowledge    | Knowledge Management         |
| Memory       | AI Memory                    |
| Integration  | External Systems             |
| Notification | Messaging                    |
| Platform     | Infrastructure               |
| Governance   | Audit & Compliance           |

---

# 5. Event Naming Standard

Event names follow:

```text
<Domain>.<Entity>.<Action>
```

Examples

```text
Identity.User.Created

Agent.Task.Assigned

Workflow.Execution.Started

Workflow.Execution.Completed

Knowledge.Document.Indexed

Memory.Session.Updated

Integration.Sync.Completed

Notification.Email.Sent
```

---

# 6. Event Registry

Each event shall include:

| Field       | Description                 |
| ----------- | --------------------------- |
| Event Name  | Unique business event       |
| Description | Business meaning            |
| Domain      | Owning business domain      |
| Producer    | Publishing service          |
| Consumers   | Subscribing services        |
| Schema      | JSON Schema                 |
| Version     | Event version               |
| Status      | Draft / Active / Deprecated |

---

# 7. Identity Events

Representative events

| Event                  |
| ---------------------- |
| Identity.User.Created  |
| Identity.User.Updated  |
| Identity.User.Disabled |
| Identity.Role.Assigned |
| Identity.Login.Success |
| Identity.Login.Failed  |

---

# 8. Agent Events

Representative events

| Event                |
| -------------------- |
| Agent.Registered     |
| Agent.Started        |
| Agent.Stopped        |
| Agent.Task.Assigned  |
| Agent.Task.Completed |
| Agent.Task.Failed    |
| Agent.Memory.Updated |

---

# 9. Workflow Events

Representative events

| Event                        |
| ---------------------------- |
| Workflow.Created             |
| Workflow.Updated             |
| Workflow.Execution.Started   |
| Workflow.Execution.Completed |
| Workflow.Execution.Cancelled |
| Workflow.Execution.Failed    |

---

# 10. Knowledge Events

Representative events

| Event                      |
| -------------------------- |
| Knowledge.Document.Created |
| Knowledge.Document.Updated |
| Knowledge.Document.Indexed |
| Knowledge.Document.Deleted |
| Knowledge.Search.Executed  |

---

# 11. Memory Events

Representative events

| Event               |
| ------------------- |
| Memory.Created      |
| Memory.Updated      |
| Memory.Archived     |
| Memory.Deleted      |
| Memory.Synchronized |

---

# 12. Integration Events

Representative events

| Event                              |
| ---------------------------------- |
| Integration.Sync.Started           |
| Integration.Sync.Completed         |
| Integration.Sync.Failed            |
| Integration.Connection.Established |
| Integration.Connection.Lost        |

---

# 13. Notification Events

Representative events

| Event                       |
| --------------------------- |
| Notification.Email.Sent     |
| Notification.SMS.Sent       |
| Notification.Push.Delivered |
| Notification.Failed         |

---

# 14. Platform Events

Representative events

| Event                     |
| ------------------------- |
| Platform.Startup          |
| Platform.Shutdown         |
| Platform.Backup.Completed |
| Platform.Health.Degraded  |
| Platform.Health.Restored  |

---

# 15. Governance Events

Representative events

| Event                      |
| -------------------------- |
| Audit.Record.Created       |
| Policy.Updated             |
| Security.Alert.Raised      |
| Compliance.Check.Completed |

---

# 16. Event Lifecycle

```text
Designed
    │
    ▼
Approved
    │
    ▼
Registered
    │
    ▼
Published
    │
    ▼
Consumed
    │
    ▼
Deprecated
    │
    ▼
Retired
```

---

# 17. Event Ownership

Every event shall identify:

* Business Owner
* Technical Owner
* Publishing Service
* Primary Consumers

Ownership shall be maintained in the Event Registry.

---

# 18. Version Management

Events shall use Semantic Versioning.

Major versions indicate breaking schema changes.

Minor versions indicate backward-compatible enhancements.

Deprecated events shall remain documented until retirement.

---

# 19. Event Catalog Governance

The Architecture Review Board shall approve:

* New event types
* Breaking changes
* Event retirement
* Naming exceptions
* Cross-domain event reuse

Duplicate business events shall be avoided.

---

# 20. Related Documents

Architecture

* OM-SOL-118 — Data Architecture
* OM-SOL-121 — Enterprise Integration Architecture

Design

* OM-DES-220 — API Design Standards
* OM-DES-223 — Event Contract Specification
* OM-DES-230 — Canonical Data Model
* OM-DES-232 — Data Contract Specification

---

# 21. Summary

The Event Catalog serves as the authoritative inventory of business events across the OneMind platform.

By governing event definitions, ownership, lifecycle, and versioning, the catalog enables consistent event-driven integration, reduces duplication, and provides a shared business language for AI agents, workflows, enterprise services, and external systems.

---

**End of Document**

**Document ID:** OM-DES-231

**Version:** 1.0

**Status:** Draft

**Milestone:** M5 – Solution Design

**Many Agents. One Mind.**
