"""
Context Ranker Tests

S4-007-002
"""

from app.context_runtime.models import (
    ContextCandidate,
    ContextLifecycle,
    ContextBudget,
    ContextAllocation,
)

from app.context_runtime.ranker import (
    DefaultContextRanker,
)


def create_candidate(
    context_id: str,
    content: str,
    lifecycle: ContextLifecycle,
):
    """
    Create test context candidate.
    """

    return ContextCandidate(
        context_id=context_id,
        content=content,
        lifecycle=lifecycle,
        budget=ContextBudget(
            max_tokens=10000,
            allocation=ContextAllocation(
                system=1000,
                memory=3000,
                knowledge=4000,
                conversation=2000,
            ),
        ),
    )


def test_rank_context_by_query_match():
    """
    Verify query relevance affects ranking.
    """

    ranker = DefaultContextRanker()

    candidates = [
        create_candidate(
            context_id="context-001",
            content="python database architecture",
            lifecycle=ContextLifecycle.ACTIVE,
        ),
        create_candidate(
            context_id="context-002",
            content="weather information",
            lifecycle=ContextLifecycle.ACTIVE,
        ),
    ]

    result = ranker.rank(
        candidates=candidates,
        query="python database",
    )

    assert result[0].context_id == (
        "context-001"
    )


def test_active_context_scores_higher():
    """
    Verify active lifecycle priority.
    """

    ranker = DefaultContextRanker()

    candidates = [
        create_candidate(
            context_id="created-context",
            content="same information",
            lifecycle=ContextLifecycle.CREATED,
        ),
        create_candidate(
            context_id="active-context",
            content="same information",
            lifecycle=ContextLifecycle.ACTIVE,
        ),
    ]

    result = ranker.rank(
        candidates=candidates,
        query="same information",
    )

    assert result[0].context_id == (
        "active-context"
    )


def test_rank_limit():
    """
    Verify top-k limit.
    """

    ranker = DefaultContextRanker()

    candidates = [
        create_candidate(
            context_id=f"context-{i}",
            content="test context",
            lifecycle=ContextLifecycle.ACTIVE,
        )
        for i in range(10)
    ]

    result = ranker.rank(
        candidates=candidates,
        query="test",
        limit=3,
    )

    assert len(result) == 3


def test_score_generation():
    """
    Verify scoring output.
    """

    ranker = DefaultContextRanker()

    candidate = create_candidate(
        context_id="score-context",
        content="context scoring test",
        lifecycle=ContextLifecycle.ACTIVE,
    )

    score = ranker.score(
        candidate=candidate,
        query="context scoring",
    )

    assert score.total_score > 0
    assert 0 <= score.query_match <= 1
    assert 0 <= score.lifecycle_score <= 1
    assert 0 <= score.budget_score <= 1
