"""
Context Relevance Scoring

S4-007-002

Provides deterministic scoring functions
for context ranking.

Future extension:
- embedding similarity
- vector score
- LLM reranking
"""

from dataclasses import dataclass

from .models import (
    ContextCandidate,
    ContextLifecycle,
)


@dataclass
class ContextScore:
    """
    Context ranking score breakdown.
    """

    query_match: float
    lifecycle_score: float
    budget_score: float
    total_score: float


def calculate_query_match_score(
    candidate: ContextCandidate,
    query: str,
) -> float:
    """
    Calculate keyword overlap score.

    Phase 1:
    simple deterministic matching.
    """

    if not query:
        return 0.0

    content = (
        candidate.content or ""
    ).lower()

    query_words = set(
        query.lower().split()
    )

    if not query_words:
        return 0.0

    matched = sum(
        1
        for word in query_words
        if word in content
    )

    return min(
        matched / len(query_words),
        1.0,
    )


def calculate_lifecycle_score(
    candidate: ContextCandidate,
) -> float:
    """
    Calculate lifecycle priority.

    Active contexts are preferred.
    """

    lifecycle_scores = {
        ContextLifecycle.ACTIVE: 1.0,
        ContextLifecycle.CREATED: 0.7,
        ContextLifecycle.STALE: 0.4,
        ContextLifecycle.ARCHIVED: 0.1,
    }

    return lifecycle_scores.get(
        candidate.lifecycle,
        0.0,
    )


def calculate_budget_score(
    candidate: ContextCandidate,
) -> float:
    """
    Calculate remaining budget score.
    """

    budget = candidate.budget

    if budget is None:
        return 0.0

    max_tokens = (
        budget.max_tokens
    )

    if max_tokens <= 0:
        return 0.0

    used_tokens = (
        budget.used_tokens
    )

    remaining = (
        max_tokens - used_tokens
    )

    if remaining <= 0:
        return 0.0

    return min(
        remaining / max_tokens,
        1.0,
    )
