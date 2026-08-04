"""
Context Selector Tests

Sprint:
    S4-007-003 Context Selector
"""

from app.context_runtime.models import (
    ContextCandidate,
    ContextLifecycle,
)

from app.context_runtime.policies import (
    SelectionPolicy,
)

from app.context_runtime.selector import (
    DefaultContextSelector,
)


def create_candidate(
    candidate_id: str,
    content: str,
    score: float,
) -> ContextCandidate:
    """
    Helper factory for test candidates.
    """

    return ContextCandidate(
        context_id=candidate_id,
        content=content,
        score=score,
        lifecycle=ContextLifecycle.ACTIVE,
        metadata={
            "source": "test"
        },
    )


def test_select_top_k():
    """
    Selector should respect max_items.
    """

    selector = DefaultContextSelector()

    candidates = [
        create_candidate(
            "a",
            "context a",
            0.95,
        ),
        create_candidate(
            "b",
            "context b",
            0.85,
        ),
        create_candidate(
            "c",
            "context c",
            0.75,
        ),
    ]

    policy = SelectionPolicy(
        max_items=2,
        max_tokens=1000,
        min_score=0.0,
    )

    result = selector.select(
        candidates,
        policy,
    )

    assert len(result.items) == 2

    assert (
        result.items[0].context_id
        == "a"
    )

    assert (
        result.items[1].context_id
        == "b"
    )


def test_filter_min_score():
    """
    Selector should remove candidates
    below score threshold.
    """

    selector = DefaultContextSelector()

    candidates = [
        create_candidate(
            "high",
            "high score",
            0.9,
        ),
        create_candidate(
            "low",
            "low score",
            0.2,
        ),
    ]

    policy = SelectionPolicy(
        min_score=0.5,
        max_items=10,
        max_tokens=1000,
    )

    result = selector.select(
        candidates,
        policy,
    )

    assert len(result.items) == 1

    assert (
        result.items[0].context_id
        == "high"
    )


def test_select_by_token_budget():
    """
    Selector should stop when token budget
    is exceeded.
    """

    selector = DefaultContextSelector()

    candidates = [
        create_candidate(
            "a",
            "a" * 100,
            0.9,
        ),
        create_candidate(
            "b",
            "b" * 100,
            0.8,
        ),
    ]

    policy = SelectionPolicy(
        max_items=10,
        max_tokens=30,
        min_score=0.0,
    )

    result = selector.select(
        candidates,
        policy,
    )

    assert len(result.items) == 1

    assert (
        result.items[0].context_id
        == "a"
    )


def test_preserve_rank_order():
    """
    Selector should preserve ranking order
    from Context Ranker.
    """

    selector = DefaultContextSelector()

    candidates = [
        create_candidate(
            "first",
            "first",
            0.95,
        ),
        create_candidate(
            "second",
            "second",
            0.80,
        ),
        create_candidate(
            "third",
            "third",
            0.70,
        ),
    ]

    policy = SelectionPolicy(
        max_items=3,
        max_tokens=1000,
        min_score=0.0,
    )

    result = selector.select(
        candidates,
        policy,
    )

    ids = [
        item.context_id
        for item in result.items
    ]

    assert ids == [
        "first",
        "second",
        "third",
    ]


def test_return_selection_metadata():
    """
    Selector should expose selection metadata.
    """

    selector = DefaultContextSelector()

    candidates = [
        create_candidate(
            "memory-1",
            "memory content",
            0.9,
        )
    ]

    policy = SelectionPolicy(
        max_items=5,
        max_tokens=1000,
        min_score=0.5,
    )

    result = selector.select(
        candidates,
        policy,
    )

    assert (
        result.metadata["selector"]
        == "default"
    )

    assert (
        result.total_score
        == 0.9
    )

    assert (
        result.total_tokens
        > 0
    )
