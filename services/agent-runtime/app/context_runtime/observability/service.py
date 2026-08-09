"""
Context Runtime Observability Service

Provides lifecycle management for Context Runtime traces,
events, timings, and metrics collection.

The service is implemented as an in-memory observability
provider and conforms to the ContextObservabilityInterface.

Sprint:
S4-010-001 Observability Interface Foundation

Author:
OneMind Platform

License:
MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from .events import ContextRuntimeEvent
from .interface import ContextObservabilityInterface
from .metrics import (
    build_metrics_snapshot,
    calculate_latency,
    update_metrics_snapshot,
)
from .models import (
    ContextRuntimeSummary,
    ContextRuntimeTrace,
    ContextStageTiming,
    ContextTraceEvent,
)


class ContextObservabilityService(
    ContextObservabilityInterface,
):
    """
    In-memory Context Runtime observability provider.

    Implements:

    - Trace lifecycle
    - Event recording
    - Stage timing
    - Metrics collection
    - Runtime summaries

    This is the first provider implementation behind
    the observability abstraction layer.

    Future providers:

    - OpenTelemetryProvider
    - PrometheusMetricsProvider
    - External telemetry backends
    """

    def __init__(self) -> None:
        self._traces: dict[
            UUID,
            ContextRuntimeTrace,
        ] = {}

    # ------------------------------------------------------------------
    # Trace lifecycle
    # ------------------------------------------------------------------

    def start_trace(
        self,
        *,
        request_id: str | None = None,
        task_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict | None = None,
    ) -> ContextRuntimeTrace:
        """
        Create and register a new runtime trace.
        """

        trace = ContextRuntimeTrace(
            request_id=request_id,
            task_id=task_id,
            agent_id=agent_id,
            metadata=metadata or {},
        )

        self._traces[
            trace.trace_id
        ] = trace

        self.record_event(
            trace.trace_id,
            ContextRuntimeEvent.CONTEXT_BUILD_STARTED,
        )

        return trace

    def get_trace(
        self,
        trace_id: UUID,
    ) -> ContextRuntimeTrace | None:
        """
        Retrieve trace by identifier.
        """

        return self._traces.get(
            trace_id
        )

    def finish_trace(
        self,
        trace_id: UUID,
        *,
        success: bool = True,
    ) -> ContextRuntimeSummary:
        """
        Complete trace execution and generate summary.
        """

        trace = self._require_trace(
            trace_id
        )

        completed_at = datetime.now(
            UTC
        )

        trace.completed_at = completed_at
        trace.success = success

        if not success:
            trace.metrics.failed_stages += 1

        self.record_event(
            trace_id,
            (
                ContextRuntimeEvent.FINISHED
                if success
                else ContextRuntimeEvent.FAILED
            ),
        )

        total_latency = calculate_latency(
            trace.started_at,
            completed_at,
        )

        return ContextRuntimeSummary(
            trace_id=trace.trace_id,
            request_id=trace.request_id,
            task_id=trace.task_id,
            agent_id=trace.agent_id,
            success=success,
            started_at=trace.started_at,
            completed_at=completed_at,
            total_latency_ms=(
                total_latency
                or 0.0
            ),
            metrics=trace.metrics,
            stage_timings=trace.stage_timings,
            event_count=len(
                trace.events
            ),
            stage_count=len(
                trace.stage_timings
            ),
        )

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def record_event(
        self,
        trace_id: UUID,
        event: ContextRuntimeEvent,
        *,
        metadata: dict | None = None,
    ) -> ContextTraceEvent:
        """
        Append an event to a trace.
        """

        trace = self._require_trace(
            trace_id
        )

        trace_event = ContextTraceEvent(
            event=event.value,
            metadata=metadata or {},
        )

        trace.events.append(
            trace_event
        )

        trace.metrics.event_count = len(
            trace.events
        )

        return trace_event

    # ------------------------------------------------------------------
    # Stage timing
    # ------------------------------------------------------------------

    def start_stage(
        self,
        trace_id: UUID,
        stage: str,
    ) -> ContextStageTiming:
        """
        Start timing for pipeline stage.
        """

        trace = self._require_trace(
            trace_id
        )

        timing = ContextStageTiming(
            stage=stage,
            started_at=datetime.now(
                UTC
            ),
        )

        trace.stage_timings.append(
            timing
        )

        trace.metrics.total_stages = len(
            trace.stage_timings
        )

        return timing

    def complete_stage(
        self,
        trace_id: UUID,
        stage: str,
    ) -> ContextStageTiming | None:
        """
        Complete timing for pipeline stage.
        """

        trace = self._require_trace(
            trace_id
        )

        completed_at = datetime.now(
            UTC
        )

        for timing in reversed(
            trace.stage_timings
        ):
            if (
                timing.stage == stage
                and timing.completed_at is None
            ):
                timing.completed_at = completed_at

                timing.latency_ms = calculate_latency(
                    timing.started_at,
                    completed_at,
                )

                trace.metrics.completed_stages = len(
                    [
                        item
                        for item in trace.stage_timings
                        if item.completed_at is not None
                    ]
                )

                return timing

        return None

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def update_metrics(
        self,
        trace_id: UUID,
        *,
        retrieved_items: int | None = None,
        ranked_items: int | None = None,
        selected_items: int | None = None,
        original_tokens: int | None = None,
        compressed_tokens: int | None = None,
    ) -> None:
        """
        Apply a partial metrics update to a trace.

        ``None`` means that the existing metric value must
        be preserved.

        This allows runtime stages to update metrics
        incrementally without resetting values produced
        by earlier stages.
        """

        trace = self._require_trace(
            trace_id
        )

        trace.metrics = update_metrics_snapshot(
            trace.metrics,
            retrieved_items=retrieved_items,
            ranked_items=ranked_items,
            selected_items=selected_items,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            event_count=len(
                trace.events
            ),
            total_stages=len(
                trace.stage_timings
            ),
            completed_stages=len(
                [
                    stage
                    for stage in trace.stage_timings
                    if stage.completed_at is not None
                ]
            ),
            failed_stages=trace.metrics.failed_stages,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require_trace(
        self,
        trace_id: UUID,
    ) -> ContextRuntimeTrace:
        """
        Return trace or raise error.
        """

        trace = self._traces.get(
            trace_id
        )

        if trace is None:
            raise ValueError(
                f"Context runtime trace not found: {trace_id}"
            )

        return trace
