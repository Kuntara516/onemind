# OM-DES-221

# REST API Specification

**Document ID:** OM-DES-221

**Document Title:** REST API Specification

**Domain:** Solution Design

**Version:** 1.0

**Status:** Draft

**Owner:** OneMind Architecture Team

**Classification:** Internal

---

# 1. Purpose

This document defines the REST API specification for the OneMind Enterprise AI Operating Platform.

It provides implementation-ready standards for RESTful services based on the API Design Standards defined in **OM-DES-220**.

This specification applies to all public, partner, internal, and administrative REST APIs.

---

# 2. References

This specification shall be read together with:

* OM-DES-220 — API Design Standards
* OM-DES-216 — Integration Domain Design
* OM-DES-219 — Observability Domain Design

---

# 3. REST Design Principles

All REST APIs shall follow these principles:

* Resource-oriented
* Stateless
* Cache-friendly
* Layered architecture
* Uniform interface
* Hypermedia optional
* JSON as default representation

---

# 4. Base URL

Production

```text
https://api.onemind.ai/api/v1
```

Development

```text
https://dev-api.onemind.ai/api/v1
```

Local

```text
http://localhost:8080/api/v1
```

---

# 5. Resource Naming

Resources use plural nouns.

Examples

```text
/users

/agents

/workflows

/memories

/knowledge

/models

/prompts

/tools

/events
```

Nested resources

```text
/workflows/{workflowId}/tasks

/agents/{agentId}/skills

/knowledge/{documentId}/chunks
```

---

# 6. CRUD Operations

| Operation      | HTTP Method | Example        |
| -------------- | ----------- | -------------- |
| Create         | POST        | `/agents`      |
| Read           | GET         | `/agents/{id}` |
| Update         | PUT         | `/agents/{id}` |
| Partial Update | PATCH       | `/agents/{id}` |
| Delete         | DELETE      | `/agents/{id}` |

---

# 7. Collection Operations

Retrieve collection

```http
GET /api/v1/agents
```

Retrieve single resource

```http
GET /api/v1/agents/{id}
```

Create resource

```http
POST /api/v1/agents
```

Delete resource

```http
DELETE /api/v1/agents/{id}
```

---

# 8. Query Parameters

Pagination

```text
?page=1&pageSize=25
```

Filtering

```text
?status=active
```

Sorting

```text
?sort=name

?sort=-createdAt
```

Searching

```text
?q=research
```

Field selection

```text
?fields=id,name,status
```

---

# 9. Request Headers

Mandatory

```http
Authorization: Bearer <token>

Content-Type: application/json

Accept: application/json

X-Correlation-ID: UUID
```

Optional

```http
If-Match

If-None-Match

Idempotency-Key
```

---

# 10. Response Headers

Representative headers

```http
Content-Type

ETag

Retry-After

Location

Cache-Control

X-RateLimit-Limit

X-RateLimit-Remaining
```

---

# 11. Request Example

```http
POST /api/v1/agents
```

```json
{
  "name": "Research Agent",
  "description": "Enterprise knowledge assistant",
  "enabled": true
}
```

---

# 12. Successful Response

```json
{
  "data": {
    "id": "a92df9d8-f98f-49b2-a6fd-f0c16bb0dfd8",
    "name": "Research Agent",
    "enabled": true
  },
  "meta": {
    "version": "v1"
  }
}
```

---

# 13. Error Response

```json
{
  "type": "validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Agent name is required."
}
```

Error responses shall conform to RFC 9457.

---

# 14. Authentication

Supported authentication methods:

* OAuth 2.0
* OpenID Connect
* JWT
* Service Account Tokens

Every request shall be authenticated unless explicitly documented otherwise.

---

# 15. Authorization

Authorization shall be enforced using RBAC.

Representative roles include:

* Platform Administrator
* Tenant Administrator
* Developer
* Operator
* Standard User
* AI Agent

Authorization decisions shall be evaluated for every request.

---

# 16. Validation

Input validation includes:

* Required fields
* Data types
* Length constraints
* Enumeration values
* Business rules
* Identifier format
* Payload size

Validation failures shall return HTTP 422.

---

# 17. Idempotency

The following operations should support idempotency:

* Workflow execution
* External integrations
* Payment-like operations
* Long-running requests

Header

```http
Idempotency-Key
```

---

# 18. Caching

GET operations may support caching.

Supported mechanisms:

* ETag
* Cache-Control
* Last-Modified

Cache invalidation shall occur after updates.

---

# 19. API Documentation

Every REST endpoint shall include:

* OpenAPI 3.1 definition
* Example requests
* Example responses
* Error examples
* Security requirements
* Rate limits
* Version history

---

# 20. Observability

Every REST request shall produce:

* Structured logs
* Metrics
* Distributed traces
* Audit records

Correlation IDs shall be propagated throughout downstream services.

---

# 21. Security Requirements

REST APIs shall implement:

* TLS 1.3
* HTTPS only
* JWT validation
* Input validation
* Output encoding
* Secret management
* Rate limiting
* Audit logging

Sensitive information shall never appear in responses.

---

# 22. OpenAPI Requirements

All REST APIs shall provide:

* OpenAPI 3.1 specification
* Machine-readable schema
* Human-readable documentation
* Example payloads
* Schema validation

OpenAPI specifications shall be maintained in source control.

---

# 23. API Lifecycle

The lifecycle of a REST API consists of:

```text
Draft

↓

Review

↓

Approved

↓

Implemented

↓

Tested

↓

Released

↓

Deprecated

↓

Retired
```

---

# 24. Implementation Checklist

Before release, verify:

* URI follows standards
* HTTP methods are correct
* OpenAPI complete
* Authentication implemented
* Authorization verified
* Validation complete
* Error handling compliant
* Logging enabled
* Metrics collected
* Tracing configured
* Security review completed

---

# 25. Related Documents

Architecture

* OM-SOL-121 — Enterprise Integration Architecture

Design

* OM-DES-220 — API Design Standards
* OM-DES-222 — MCP Tool Specification
* OM-DES-223 — Event Contract Specification
* OM-DES-225 — API Versioning & Compatibility

---

# 26. Summary

This specification defines the implementation standards for REST APIs within the OneMind platform.

Together with OM-DES-220, it ensures that all REST services provide consistent interfaces, standardized security, predictable behavior, comprehensive observability, and long-term maintainability across the enterprise platform.

---

**End of Document**

**Document ID:** OM-DES-221

**Version:** 1.0

**Status:** Draft

**Milestone:** M5 – Solution Design

**Many Agents. One Mind.**
