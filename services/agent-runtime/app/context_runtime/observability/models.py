"""
Context Runtime Observability Models

Pydantic models used for tracing, timing, and metrics collection
within the Context Runtime execution pipeline.

Sprint:
    S4-009 Context Runtime Observability

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ContextStageTiming(BaseModel):
    """
    Timing information for a single pipeline stage.
    """

    stage: str = Field(
        ...,
        description="Pipeline stage name.",
    )

    started_at: datetime | None = Field(
        default=None,
        description="UTC timestamp when the stage started.",
    )

    completed_at: datetime | None = Field(
        default=None,
        description="UTC timestamp when the stage completed.",
    )

    latency_ms: float | None = Field(
        default=None,
        ge=0,
        description="Execution latency in milliseconds.",
    )


class ContextMetricsSnapshot(BaseModel):
    """
    Runtime metrics collected during context execution.
    """

    retrieved_items: int = Field(
        default=0,
        ge=0,
    )

    ranked_items: int = Field(
        default=0,
        ge=0,
    )

    selected_items: int = Field(
        default=0,
        ge=0,
    )

    original_tokens: int = Field(
        default=0,
        ge=0,
    )

    compressed_tokens: int = Field(
        default=0,
        ge=0,
    )

    compression_ratio: float | None = Field(
        default=None,
        ge=0,
    )

    selection_ratio: float | None = Field(
        default=None,
        ge=0,
    )

    token_reduction: int | None = Field(
        default=None,
    )


class ContextTraceEvent(BaseModel):
    """
    Individual event emitted during Context Runtime execution.
    """

    event: str = Field(
        ...,
        description="Event name.",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC event timestamp.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional event metadata.",
    )


class ContextRuntimeTrace(BaseModel):
    """
    Complete execution trace for a single Context Runtime invocation.
    """

    trace_id: UUID = Field(
        default_factory=uuid4,
        description="Unique trace identifier.",
    )

    request_id: str | None = Field(
        default=None,
    )

    task_id: str | None = Field(
        default=None,
    )

    agent_id: str | None = Field(
        default=None,
    )

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    completed_at: datetime | None = Field(
        default=None,
    )

    success: bool | None = Field(
        default=None,
    )

    events: list[ContextTraceEvent] = Field(
        default_factory=list,
    )

    stage_timings: list[ContextStageTiming] = Field(
        default_factory=list,
    )

    metrics: ContextMetricsSnapshot = Field(
        default_factory=ContextMetricsSnapshot,
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ContextRuntimeSummary(BaseModel):
    """
    High-level execution summary generated after a trace finishes.
    """

    trace_id: UUID

    request_id: str | None = None

    task_id: str | None = None

    agent_id: str | None = None

    success: bool

    started_at: datetime

    completed_at: datetime

    total_latency_ms: float = Field(
        ge=0,
    )

    metrics: ContextMetricsSnapshot

    stage_timings: list[ContextStageTiming] = Field(
        default_factory=list,
    )
