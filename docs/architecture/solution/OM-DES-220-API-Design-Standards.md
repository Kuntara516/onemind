# OM-DES-220

# API Design Standards

**Document ID:** OM-DES-220

**Document Title:** API Design Standards

**Domain:** Solution Design

**Version:** 1.0

**Status:** Draft

**Owner:** OneMind Architecture Team

**Classification:** Internal

---

# 1. Purpose

This document defines the API Design Standards for the OneMind Enterprise AI Operating Platform.

It establishes a consistent, secure, maintainable, and implementation-ready approach for designing all platform APIs.

These standards apply to:

* REST APIs
* Internal Service APIs
* Agent APIs
* MCP Tool Interfaces
* Administrative APIs
* Future API technologies

---

# 2. Design Objectives

All APIs shall be:

* Consistent
* Predictable
* Secure
* Versioned
* Observable
* Backward Compatible
* Well Documented
* Implementation Ready

API consumers should be able to understand any OneMind API without learning different conventions.

---

# 3. API Design Principles

## Consistency

All APIs shall follow identical conventions.

Examples include:

* URI naming
* HTTP methods
* Response format
* Error format
* Authentication
* Pagination

---

## Simplicity

APIs should expose business capabilities rather than implementation details.

Avoid unnecessary nesting and complex request structures.

---

## Stateless

Every request shall contain all information required for processing.

Server-side session state should be avoided unless explicitly required.

---

## Resource-Oriented Design

Resources represent business entities.

Examples:

```text
/users

/agents

/workflows

/knowledge

/memories

/models
```

Avoid action-oriented endpoints.

Preferred:

```text
POST /workflows
```

Avoid:

```text
/createWorkflow
```

---

# 4. URI Standards

Rules:

* lowercase only
* plural resource names
* hyphen-separated words
* nouns instead of verbs

Good

```text
/api/v1/users

/api/v1/workflows

/api/v1/knowledge-items
```

Avoid

```text
/getUser

/CreateAgent

/workflow_create
```

---

# 5. HTTP Method Standards

| Method | Purpose                            |
| ------ | ---------------------------------- |
| GET    | Retrieve resources                 |
| POST   | Create resource or execute command |
| PUT    | Replace resource                   |
| PATCH  | Partial update                     |
| DELETE | Remove resource                    |

Example

```http
GET /api/v1/agents

POST /api/v1/agents

GET /api/v1/agents/{id}

PATCH /api/v1/agents/{id}

DELETE /api/v1/agents/{id}
```

---

# 6. HTTP Status Codes

| Code | Meaning               |
| ---: | --------------------- |
|  200 | Success               |
|  201 | Created               |
|  202 | Accepted              |
|  204 | No Content            |
|  400 | Bad Request           |
|  401 | Unauthorized          |
|  403 | Forbidden             |
|  404 | Not Found             |
|  409 | Conflict              |
|  422 | Validation Error      |
|  429 | Too Many Requests     |
|  500 | Internal Server Error |
|  503 | Service Unavailable   |

Use standard HTTP semantics.

Avoid inventing custom status codes.

---

# 7. Request Format

Example

```json
{
  "name": "Research Agent",
  "description": "Enterprise research assistant",
  "enabled": true
}
```

Rules

* camelCase JSON properties
* UTF-8
* ISO-8601 timestamps
* UUID identifiers
* Explicit null handling

---

# 8. Response Format

Successful responses shall follow a consistent structure.

Example

```json
{
  "data": {
    "id": "7d5d7f5b-3b6f-4d4d-92d5-ec5dbd0a77fa",
    "name": "Research Agent"
  },
  "meta": {
    "version": "v1"
  }
}
```

---

# 9. Error Response Standard

All errors shall follow a consistent format based on **RFC 9457 Problem Details**.

Example

```json
{
  "type": "validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Agent name is required.",
  "instance": "/api/v1/agents"
}
```

Do not expose internal stack traces.

---

# 10. Pagination

Large collections shall support pagination.

Example

```text
GET /api/v1/agents?page=1&pageSize=50
```

Response

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalItems": 320,
    "totalPages": 7
  }
}
```

---

# 11. Filtering

Example

```text
GET /api/v1/workflows?status=active
```

Multiple filters

```text
?status=active&type=approval
```

---

# 12. Sorting

Example

```text
?sort=name

?sort=-createdAt
```

Ascending

```text
sort=name
```

Descending

```text
sort=-name
```

---

# 13. Searching

Example

```text
GET /api/v1/knowledge?q=architecture
```

Support full-text search where appropriate.

---

# 14. Authentication

Supported mechanisms:

* OAuth 2.0
* OpenID Connect
* JWT
* API Keys (internal only)
* Service Accounts

Anonymous APIs are prohibited unless explicitly approved.

---

# 15. Authorization

Authorization shall use Role-Based Access Control (RBAC).

Examples:

* Platform Admin
* Tenant Admin
* Developer
* Operator
* User
* AI Agent

Authorization must be evaluated on every request.

---

# 16. API Versioning

URI versioning shall be used.

Example

```text
/api/v1/

/api/v2/
```

Breaking changes require a new major version.

Minor enhancements shall remain backward compatible.

---

# 17. Idempotency

Operations that may be retried should support idempotency.

Example

```http
Idempotency-Key:
```

Required for:

* Payment-like operations
* Workflow execution
* Long-running jobs
* External integrations

---

# 18. Correlation ID

Every request shall include a Correlation ID.

Header

```http
X-Correlation-ID
```

This value shall propagate across:

* APIs
* Events
* Workflows
* Agents
* Logs
* Traces

---

# 19. Rate Limiting

Representative headers

```http
X-RateLimit-Limit

X-RateLimit-Remaining

Retry-After
```

Rate limiting policies shall be configurable.

---

# 20. API Documentation

Every API shall provide:

* OpenAPI 3.1 Specification
* Request examples
* Response examples
* Error examples
* Authentication requirements
* Change history

---

# 21. Observability

Every API shall emit:

* Metrics
* Structured Logs
* Distributed Traces
* Audit Records

API execution shall be fully observable.

---

# 22. Security Requirements

APIs shall implement:

* TLS 1.3
* Input validation
* Output encoding
* Rate limiting
* Secret management
* Audit logging
* Sensitive data masking
* Principle of least privilege

---

# 23. Deprecation Policy

Deprecated APIs shall:

* Be documented
* Provide migration guidance
* Include deprecation headers
* Remain available during the supported transition period

Removal shall occur only in the next major version.

---

# 24. API Design Checklist

Before publishing an API, verify:

* Resource-oriented URI
* Correct HTTP method
* Standard status codes
* Consistent JSON schema
* Authentication
* Authorization
* Pagination (if applicable)
* Error handling
* OpenAPI documentation
* Logging
* Metrics
* Tracing
* Versioning
* Security review

---

# 25. Related Documents

Architecture

* OM-SOL-121 — Enterprise Integration Architecture
* OM-SOL-123 — Observability Architecture

Design

* OM-DES-216 — Integration Domain Design
* OM-DES-219 — Observability Domain Design
* OM-DES-221 — REST API Specification
* OM-DES-222 — MCP Tool Specification
* OM-DES-223 — Event Contract Specification
* OM-DES-225 — API Versioning & Compatibility

---

# 26. Summary

The API Design Standards establish a unified engineering standard for all APIs within the OneMind platform.

By defining consistent conventions for resource modeling, HTTP semantics, security, versioning, observability, and documentation, these standards enable teams to design and implement APIs that are predictable, interoperable, and maintainable across the entire platform lifecycle.

---

**End of Document**

**Document ID:** OM-DES-220

**Version:** 1.0

**Status:** Draft

**Milestone:** M5 – Solution Design

**Many Agents. One Mind.**
