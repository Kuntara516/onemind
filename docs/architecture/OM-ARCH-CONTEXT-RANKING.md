# OM-ARCH-CONTEXT-RANKING

## Context Ranking Architecture

**Project:** OneMind  
**Sprint:** Sprint 4 - Context Intelligence & Retrieval Pipeline  
**Component:** Context Ranking Layer  
**Status:** Architecture Frozen  
**Version:** v0.8.4-s4-context-ranking

---

# 1. Overview

Context Ranking Layer เป็นองค์ประกอบหนึ่งของ Context Intelligence Pipeline ทำหน้าที่จัดลำดับความสำคัญของข้อมูลที่ถูก Retrieval มา เพื่อให้ Context Orchestrator สามารถเลือก Context ที่เหมาะสมที่สุดก่อนส่งต่อให้ Agent Runtime

ในระบบ Multi-Agent การค้นคืนข้อมูลเพียงอย่างเดียวไม่เพียงพอ เนื่องจาก Retrieval อาจคืนข้อมูลจำนวนมากที่มี relevance แตกต่างกัน

Context Ranking จึงทำหน้าที่:

- ประเมินความเกี่ยวข้องของข้อมูล
- จัดลำดับ candidate contexts
- เพิ่ม priority ให้ข้อมูลที่เหมาะสม
- เตรียม context สำหรับ compression และ token budgeting

---

# 2. Position in Context Intelligence Pipeline

            User Request
                 |
                 v
      +---------------------+
      | Context Builder      |
      +---------------------+
                 |
                 v
      +---------------------+
      | Retrieval Pipeline   |
      +---------------------+
                 |
                 v
      +---------------------+
      | Context Ranking      |
      +---------------------+
                 |
                 v
      +---------------------+
      | Context Compression  |
      +---------------------+
                 |
                 v
      +---------------------+
      | Token Budget Manager |
      +---------------------+
                 |
                 v
           Agent Runtime

---

# 3. Design Goals

## 3.1 Separation of Responsibility

Context Ranking รับผิดชอบเฉพาะ:

- scoring
- ordering
- prioritization

ไม่รับผิดชอบ:

- retrieval
- memory storage
- knowledge storage
- context assembly

---

## 3.2 Strategy Based Design

Ranking ถูกออกแบบเป็น Strategy Pattern เพื่อรองรับ:

- relevance ranking
- semantic ranking
- time-aware ranking
- user preference ranking
- hybrid ranking

ตัวอย่าง:


ContextRankingService

    |
    v

RankingStrategy Interface

    |
    +----------------+
    |
    v

DefaultRankingStrategy
SemanticRankingStrategy
HybridRankingStrategy


---

# 4. Component Architecture


context/
|
+-- ranking/
|
+-- models.py
|
+-- interface.py
|
+-- service.py
|
+-- strategies/
| |
| +-- default.py
|
+-- tests/


---

# 5. Data Model

## RankingRequest

Input สำหรับ ranking pipeline

```python
class RankingRequest:

    candidates:
        list[ContextCandidate]

    query:
        str

    metadata:
        dict
RankingResult

Output จาก ranking layer

class RankingResult:

    ranked_candidates:
        list[ContextCandidate]

    scores:
        dict

    metadata:
        dict
6. Ranking Interface

Contract:

class ContextRankingInterface:

    async def rank(
        request: RankingRequest
    ) -> RankingResult:
        pass

Interface นี้ทำให้สามารถเปลี่ยน ranking algorithm ได้โดยไม่กระทบ orchestration layer

7. Default Ranking Strategy

Default strategy ใช้ scoring model แบบ lightweight

Final Score =
    relevance_score
    +
    importance_score
    +
    recency_score

ตัวอย่าง:

Candidate A

relevance:
0.8

importance:
0.7

recency:
0.9


score:

0.8 + 0.7 + 0.9

= 2.4
8. Ranking Flow
RetrievalResult

        |
        v

Context Candidates

        |
        v

RankingRequest

        |
        v

Ranking Strategy

        |
        v

Score Calculation

        |
        v

Sort Descending

        |
        v

RankingResult
9. Integration with Context Orchestrator

ก่อน S4-004:

Context Orchestrator

        |
        v

Retrieval

        |
        v

ContextResult

หลัง S4-004:

Context Orchestrator

        |
        v

Retrieval Service

        |
        v

Ranking Service

        |
        v

Ranked Context

        |
        v

ContextResult
10. Service Responsibilities
ContextRankingService

หน้าที่:

รับ RankingRequest
เรียก Ranking Strategy
ส่งคืน RankingResult

Pseudo flow:

async def rank(request):

    result = await strategy.rank(
        request
    )

    return result
11. Future Extensions
Semantic Ranking

ใช้ embedding similarity:

Query Embedding

        |
        v

Candidate Embedding

        |
        v

Cosine Similarity

        |
        v

Ranking Score
User Preference Ranking

เพิ่ม personalized context:

Ranking Score =

semantic relevance
+
user preference
+
historical usage
Learning Based Ranking

รองรับ:

feedback loop
reinforcement signals
agent success metrics
12. Testing Strategy

Covered:

test_default_context_ranking_orders_candidates

test_default_context_ranking_calculates_score

test_context_ranking_service_delegates

test_context_ranking_empty_candidates

Validation:

ordering correctness
score calculation
service delegation
empty input handling
13. Current Limitations

Current implementation:

deterministic scoring
no ML ranking model
no embedding reranking
no user personalization

These capabilities are reserved for future Context Intelligence iterations.

14. Architecture Decision Record
ADR-S4-004-001

Decision:

Use independent Context Ranking Layer between Retrieval and Context Orchestration.

Reason:

keep retrieval simple
enable ranking evolution
support multiple ranking strategies
prepare for intelligent context selection
15. Summary

Context Ranking Layer completes the third intelligence stage of OneMind Context Pipeline.

Current pipeline:

Memory
  |
Knowledge
  |
Retrieval
  |
Ranking
  |
Orchestration
  |
Agent Runtime

This establishes the foundation for future:

Context Compression
Token Budget Optimization
Adaptive Agent Memory
Intelligent Context Selection