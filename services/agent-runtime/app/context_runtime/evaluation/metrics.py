"""
Context Runtime Evaluation Metrics

Stateless metric calculation functions
for Context Quality Evaluation.

Sprint:
    S4-011-001 Context Quality Evaluation Foundation

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations


def calculate_relevance_score(
    relevant_items: int,
    selected_items: int,
) -> float:
    """
    Calculate relevance score.

    Formula:

        relevant_items / selected_items
    """

    if selected_items <= 0:
        return 0.0

    return min(
        relevant_items / selected_items,
        1.0,
    )


def calculate_coverage_score(
    selected_items: int,
    retrieved_items: int,
) -> float:
    """
    Calculate coverage score.

    Formula:

        selected_items / retrieved_items
    """

    if retrieved_items <= 0:
        return 0.0

    return min(
        selected_items / retrieved_items,
        1.0,
    )


def calculate_diversity_score(
    duplicate_items: int,
    selected_items: int,
) -> float:
    """
    Calculate diversity score.

    Formula:

        1 - duplicate_ratio
    """

    if selected_items <= 0:
        return 0.0

    duplicate_ratio = (
        duplicate_items / selected_items
    )

    return max(
        1.0 - duplicate_ratio,
        0.0,
    )


def calculate_compression_score(
    original_tokens: int,
    compressed_tokens: int,
) -> float:
    """
    Calculate compression efficiency.

    Formula:

        1 - compression_ratio
    """

    if original_tokens <= 0:
        return 0.0

    ratio = (
        compressed_tokens /
        original_tokens
    )

    return max(
        min(1.0 - ratio, 1.0),
        0.0,
    )


def calculate_utility_score(
    *,
    success: bool,
    context_score: float,
) -> float:
    """
    Calculate execution utility.

    Utility combines:
    - execution success
    - context quality
    """

    success_factor = (
        1.0
        if success
        else 0.0
    )

    return (
        success_factor *
        context_score
    )


def calculate_overall_score(
    *,
    relevance_score: float,
    coverage_score: float,
    diversity_score: float,
    compression_score: float,
    utility_score: float,
) -> float:
    """
    Calculate weighted overall quality score.

    Initial weights are intentionally simple
    and can evolve with evaluation feedback.
    """

    score = (
        relevance_score * 0.25
        +
        coverage_score * 0.20
        +
        diversity_score * 0.20
        +
        compression_score * 0.15
        +
        utility_score * 0.20
    )

    return min(
        max(score, 0.0),
        1.0,
    )
