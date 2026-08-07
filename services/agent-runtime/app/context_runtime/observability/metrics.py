"""
Context Runtime Observability Metrics

Utility functions for calculating runtime metrics used by the
Context Runtime observability subsystem.

These functions are intentionally stateless and side-effect free.

Sprint:
    S4-009 Context Runtime Observability

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from datetime import datetime

from .models import ContextMetricsSnapshot


def calculate_latency(
    started_at: datetime | None,
    completed_at: datetime | None,
) -> float | None:
    """
    Calculate elapsed time in milliseconds.

    Args:
        started_at:
            Stage start timestamp.

        completed_at:
            Stage completion timestamp.

    Returns:
        Latency in milliseconds or None if timestamps are incomplete.
    """
    if started_at is None or completed_at is None:
        return None

    latency = (completed_at - started_at).total_seconds() * 1000

    return max(latency, 0.0)


def calculate_compression_ratio(
    original_tokens: int,
    compressed_tokens: int,
) -> float | None:
    """
    Calculate compression ratio.

    Formula:

        compressed_tokens / original_tokens

    Examples:

        1000 -> 700 = 0.70
        500 -> 250 = 0.50

    Returns:
        Compression ratio or None if original_tokens is zero.
    """
    if original_tokens <= 0:
        return None

    return compressed_tokens / original_tokens


def calculate_selection_ratio(
    retrieved_items: int,
    selected_items: int,
) -> float | None:
    """
    Calculate selection ratio.

    Formula:

        selected_items / retrieved_items

    Returns:
        Selection ratio or None if retrieved_items is zero.
    """
    if retrieved_items <= 0:
        return None

    return selected_items / retrieved_items


def calculate_token_reduction(
    original_tokens: int,
    compressed_tokens: int,
) -> int:
    """
    Calculate the number of removed tokens.

    Returns:
        original_tokens - compressed_tokens

    Never returns a negative value.
    """
    return max(original_tokens - compressed_tokens, 0)


def build_metrics_snapshot(
    *,
    retrieved_items: int = 0,
    ranked_items: int = 0,
    selected_items: int = 0,
    original_tokens: int = 0,
    compressed_tokens: int = 0,
) -> ContextMetricsSnapshot:
    """
    Build a fully-populated metrics snapshot.

    Derived metrics are calculated automatically.

    Args:
        retrieved_items:
            Number of retrieved context candidates.

        ranked_items:
            Number of ranked candidates.

        selected_items:
            Number of selected context items.

        original_tokens:
            Token count before compression.

        compressed_tokens:
            Token count after compression.

    Returns:
        ContextMetricsSnapshot
    """
    return ContextMetricsSnapshot(
        retrieved_items=retrieved_items,
        ranked_items=ranked_items,
        selected_items=selected_items,
        original_tokens=original_tokens,
        compressed_tokens=compressed_tokens,
        compression_ratio=calculate_compression_ratio(
            original_tokens,
            compressed_tokens,
        ),
        selection_ratio=calculate_selection_ratio(
            retrieved_items,
            selected_items,
        ),
        token_reduction=calculate_token_reduction(
            original_tokens,
            compressed_tokens,
        ),
    )


def update_metrics_snapshot(
    snapshot: ContextMetricsSnapshot,
    *,
    retrieved_items: int | None = None,
    ranked_items: int | None = None,
    selected_items: int | None = None,
    original_tokens: int | None = None,
    compressed_tokens: int | None = None,
) -> ContextMetricsSnapshot:
    """
    Return an updated metrics snapshot.

    Only explicitly provided values are replaced.
    Derived metrics are recalculated automatically.
    """
    retrieved = (
        snapshot.retrieved_items
        if retrieved_items is None
        else retrieved_items
    )

    ranked = (
        snapshot.ranked_items
        if ranked_items is None
        else ranked_items
    )

    selected = (
        snapshot.selected_items
        if selected_items is None
        else selected_items
    )

    original = (
        snapshot.original_tokens
        if original_tokens is None
        else original_tokens
    )

    compressed = (
        snapshot.compressed_tokens
        if compressed_tokens is None
        else compressed_tokens
    )

    return build_metrics_snapshot(
        retrieved_items=retrieved,
        ranked_items=ranked,
        selected_items=selected,
        original_tokens=original,
        compressed_tokens=compressed,
    )
