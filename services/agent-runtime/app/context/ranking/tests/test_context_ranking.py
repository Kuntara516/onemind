"""
Context Ranking Tests.

Validates Context Ranking & Prioritization Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

import pytest

from app.context.ranking.models import (
    ContextCandidate,
    RankingRequest,
)

from app.context.ranking.service import (
    ContextRankingService,
)

from app.context.ranking.strategies.default import (
    DefaultContextRanking,
)


@pytest.mark.anyio
async def test_default_context_ranking_orders_candidates():
    """
    Validate candidates are ordered by ranking score.
    """

    strategy = DefaultContextRanking()

    result = await strategy.rank(
        RankingRequest(
            candidates=[
                ContextCandidate(
                    id="low",
                    content="Low priority context",
                    metadata={
                        "relevance": 0.5,
                    },
                ),
                ContextCandidate(
                    id="high",
                    content="High priority context",
                    metadata={
                        "relevance": 1.0,
                        "importance": 2.0,
                    },
                ),
            ]
        )
    )

    assert len(result.ranked_contexts) == 2

    assert (
        result.ranked_contexts[0]
        .candidate
        .id
        == "high"
    )

    assert (
        result.ranked_contexts[0]
        .score
        .total
        > result.ranked_contexts[1]
        .score
        .total
    )


@pytest.mark.anyio
async def test_default_context_ranking_calculates_score():
    """
    Validate ranking score calculation.
    """

    strategy = DefaultContextRanking()

    result = await strategy.rank(
        RankingRequest(
            candidates=[
                ContextCandidate(
                    id="context-1",
                    content="Important context",
                    metadata={
                        "relevance": 1.0,
                        "recency": 0.5,
                        "importance": 2.0,
                        "priority": 1.5,
                    },
                )
            ]
        )
    )

    score = (
        result.ranked_contexts[0]
        .score
    )

    assert score.relevance == 1.0
    assert score.recency == 0.5
    assert score.importance == 2.0
    assert score.priority == 1.5
    assert score.total == 5.0


@pytest.mark.anyio
async def test_context_ranking_service_delegates():
    """
    Validate ranking service delegates
    to ranking strategy.
    """

    strategy = DefaultContextRanking()

    service = ContextRankingService(
        strategy,
    )

    result = await service.rank(
        RankingRequest(
            candidates=[
                ContextCandidate(
                    id="service-test",
                    content="Service delegation test",
                )
            ]
        )
    )

    assert len(result.ranked_contexts) == 1

    assert (
        result.ranked_contexts[0]
        .candidate
        .id
        == "service-test"
    )


@pytest.mark.anyio
async def test_context_ranking_empty_candidates():
    """
    Validate empty ranking request.
    """

    strategy = DefaultContextRanking()

    result = await strategy.rank(
        RankingRequest()
    )

    assert result.ranked_contexts == []
