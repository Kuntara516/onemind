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

    latency = (
        completed_at - started_at
    ).total_seconds() * 1000

    return max(latency, 0.0)


def calculate_compression_ratio(
    original_tokens: int,
    compressed_tokens: int,
) -> float | None:
    """
    Calculate compression ratio.

    Formula:

        compressed_tokens / original_tokens

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
    Calculate token reduction.

    Returns:
        Number of removed tokens.
    """

    return max(
        original_tokens - compressed_tokens,
        0,
    )


# ----------------------------------------------------------------------
# Observability Health Metrics
# ----------------------------------------------------------------------


def calculate_stage_completion_ratio(
    total_stages: int,
    completed_stages: int,
) -> float | None:
    """
    Calculate completed stage ratio.

    Formula:

        completed_stages / total_stages

    Returns:
        Completion ratio or None when no stages exist.
    """

    if total_stages <= 0:
        return None

    return completed_stages / total_stages


def calculate_pipeline_health(
    total_stages: int,
    completed_stages: int,
    failed_stages: int,
) -> float | None:
    """
    Calculate pipeline health score.

    Formula:

        completed_stages /
        (completed_stages + failed_stages)

    Returns:
        Health score between 0 and 1.
    """

    executed_stages = (
        completed_stages +
        failed_stages
    )

    if executed_stages <= 0:
        return None

    return completed_stages / executed_stages


# ----------------------------------------------------------------------
# Snapshot Builders
# ----------------------------------------------------------------------


def build_metrics_snapshot(
    *,
    retrieved_items: int = 0,
    ranked_items: int = 0,
    selected_items: int = 0,
    original_tokens: int = 0,
    compressed_tokens: int = 0,
    event_count: int = 0,
    total_stages: int = 0,
    completed_stages: int = 0,
    failed_stages: int = 0,
) -> ContextMetricsSnapshot:
    """
    Build a fully-populated metrics snapshot.

    Derived metrics are calculated automatically.
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

        event_count=event_count,
        total_stages=total_stages,
        completed_stages=completed_stages,
        failed_stages=failed_stages,
    )


def update_metrics_snapshot(
    snapshot: ContextMetricsSnapshot,
    *,
    retrieved_items: int | None = None,
    ranked_items: int | None = None,
    selected_items: int | None = None,
    original_tokens: int | None = None,
    compressed_tokens: int | None = None,
    event_count: int | None = None,
    total_stages: int | None = None,
    completed_stages: int | None = None,
    failed_stages: int | None = None,
) -> ContextMetricsSnapshot:
    """
    Return an updated metrics snapshot.

    Only explicitly provided values are replaced.
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

    events = (
        snapshot.event_count
        if event_count is None
        else event_count
    )

    stages = (
        snapshot.total_stages
        if total_stages is None
        else total_stages
    )

    completed = (
        snapshot.completed_stages
        if completed_stages is None
        else completed_stages
    )

    failed = (
        snapshot.failed_stages
        if failed_stages is None
        else failed_stages
    )

    return build_metrics_snapshot(
        retrieved_items=retrieved,
        ranked_items=ranked,
        selected_items=selected,
        original_tokens=original,
        compressed_tokens=compressed,
        event_count=events,
        total_stages=stages,
        completed_stages=completed,
        failed_stages=failed,
    )
