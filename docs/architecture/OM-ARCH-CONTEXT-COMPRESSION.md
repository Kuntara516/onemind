# OM-ARCH-CONTEXT-COMPRESSION

## Context Compression Architecture

**Project:** OneMind  
**Sprint:** Sprint 4 - Context Intelligence & Retrieval Pipeline  
**Component:** Context Compression Layer  
**Status:** Architecture Frozen Draft

---

# 1. Overview

Context Compression Layer เป็นองค์ประกอบหนึ่งของ Context Intelligence Pipeline ทำหน้าที่ลดขนาดของ context ที่ถูกสร้างจาก retrieval และ ranking ให้เหมาะสมกับข้อจำกัดของ Agent Runtime

เป้าหมายหลัก:

- ลด token consumption
- รักษาข้อมูลที่มีความสำคัญสูง
- ควบคุม context window usage
- เตรียม context ที่เหมาะสมก่อนส่งให้ Agent Execution Layer

Compression Layer ไม่ได้ทำหน้าที่สร้างข้อมูลใหม่ แต่ทำหน้าที่ optimize context ที่มีอยู่แล้ว

---

# 2. Position in Context Intelligence Pipeline

                Context Intelligence Layer


                    Context Request
                          |
                          v

                Retrieval Pipeline
                     (S4-002)
                          |
                          v

             Context Orchestration
                     (S4-003)
                          |
                          v

                Context Ranking
                     (S4-004)
                          |
                          v

             Context Compression
                     (S4-005)
                          |
                          v

                Optimized Context
                          |
                          v

                   Agent Runtime

---

# 3. Design Goals

## 3.1 Token Optimization

Compression ต้องสามารถลดจำนวน token ของ context โดยยังรักษาข้อมูลสำคัญ

ตัวอย่าง:

Before:


Context Candidates:

A - priority 0.95 - 500 tokens
B - priority 0.80 - 400 tokens
C - priority 0.20 - 300 tokens

Total:
1200 tokens


After:


Compressed Context:

A
B

Total:
900 tokens


---

## 3.2 Priority Preservation

Compression ต้องรักษาข้อมูลที่ถูกจัดอันดับสูงจาก Context Ranking Layer

Priority score จาก ranking layer จะถูกใช้เป็น input สำหรับ compression decision


Ranking Score

    |
    v

Compression Decision

    |
    v

Selected Context


---

## 3.3 Strategy Abstraction

Compression implementation ต้องไม่ผูกกับ algorithm เดียว

รองรับ:

- rule-based compression
- token budget compression
- LLM summarization
- semantic compression
- domain-specific compression

ผ่าน interface contract

---

# 4. Component Architecture


context/compression

├── models.py
│
├── interface.py
│
├── service.py
│
├── strategies
│ └── default.py
│
└── tests


---

# 5. Component Responsibilities

## 5.1 Compression Models

Location:


app/context/compression/models.py


Responsibilities:

- Define compression request
- Define compression candidates
- Define compression result

Models:


CompressionRequest

|
+-- candidates
+-- token_budget
+-- metadata

CompressionResult

|
+-- compressed_candidates
+-- token statistics
+-- compression metadata

---

# 5.2 Compression Interface

Location:


app/context/compression/interface.py


Responsibilities:

Define contract for compression strategies.

Interface:

```python
class ContextCompressionInterface:

    async def compress(
        request: CompressionRequest
    ) -> CompressionResult
5.3 Compression Service

Location:

app/context/compression/service.py

Responsibilities:

Provide facade API
Hide strategy implementation
Delegate compression execution

Flow:

CompressionRequest

        |
        v

ContextCompressionService

        |
        v

CompressionStrategy

        |
        v

CompressionResult
5.4 Default Compression Strategy

Location:

app/context/compression/strategies/default.py

Responsibilities:

Initial compression implementation.

Current capabilities:

Sort candidates by priority
Respect token budget
Remove low-value candidates
Generate compression metadata

Algorithm:

Input Candidates

        |
        v

Sort by priority_score

        |
        v

Select until token budget reached

        |
        v

Return compressed candidates
6. Data Flow
Retrieval Result

        |
        v

Context Ranking Result

        |
        v

CompressionRequest

        |
        v

Compression Service

        |
        v

Compression Strategy

        |
        v

CompressionResult

        |
        v

Agent Context
7. Compression Decision Model

Current strategy:

candidate.priority_score
            +
candidate.estimated_tokens
            +
available_token_budget

            |
            v

Selection Decision

Priority:

Higher score
    |
    v
Higher retention probability
8. Future Extensions
8.1 Semantic Compression

Future implementation:

Context

 |
 v

Embedding Similarity

 |
 v

Duplicate Removal

 |
 v

Compressed Context
8.2 LLM Based Summarization

Possible future strategy:

Large Context

 |
 v

LLM Compressor

 |
 v

Summary Context
8.3 Adaptive Compression

Compression level can depend on:

Agent type
Task complexity
Token budget
Model capability

Example:

Simple Task

Low Compression


Complex Task

High Compression
9. Integration with Agent Runtime

Final execution flow:

User Request

      |
      v

Agent Runtime

      |
      v

Context Intelligence

      |
      +--> Retrieval
      |
      +--> Ranking
      |
      +--> Compression

      |
      v

Optimized Agent Context

      |
      v

Agent Execution
10. Testing Strategy

Compression Layer tests:

test_context_compression.py

Covered scenarios:

token budget enforcement
priority preservation
service delegation
empty candidate handling

Expected:

4 passed
11. Sprint 4 Status
Component	Status
Retrieval Pipeline	Complete
Context Orchestration	Complete
Context Ranking	Complete
Context Compression	Complete
12. Summary

Context Compression Layer completes the optimization stage of OneMind Context Intelligence Pipeline.

It provides:

controlled context size
token-aware optimization
strategy abstraction
future LLM compression support

This layer prepares high-quality, efficient context before Agent Runtime execution.