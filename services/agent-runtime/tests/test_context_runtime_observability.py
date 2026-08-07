"""
Context Runtime Observability Tests

Sprint:
    S4-009 Context Runtime Observability

Coverage:

- Trace lifecycle
- Event tracking
- Stage timing
- Metrics collection
- Integration observability propagation
"""

from __future__ import annotations

from time import sleep

from app.context_runtime.observability import (
    ContextObservabilityService,
    ContextRuntimeEvent,
)

from app.context_runtime.observability.metrics import (
    calculate_pipeline_health,
)


def test_trace_lifecycle():
    """
    Verify trace creation and completion lifecycle.
    """

    service = ContextObservabilityService()

    trace = service.start_trace(
        request_id="request-001",
        task_id="task-001",
        agent_id="agent-001",
    )

    assert trace.trace_id is not None
    assert trace.completed_at is None

    summary = service.finish_trace(
        trace.trace_id
    )

    assert summary.success is True
    assert summary.completed_at is not None
    assert summary.total_latency_ms >= 0


def test_event_tracking():
    """
    Verify runtime event collection.
    """

    service = ContextObservabilityService()

    trace = service.start_trace()

    service.record_event(
        trace.trace_id,
        ContextRuntimeEvent.RETRIEVAL_STARTED,
    )

    service.record_event(
        trace.trace_id,
        ContextRuntimeEvent.RETRIEVAL_COMPLETED,
        metadata={
            "items": 5,
        },
    )

    stored = service.get_trace(
        trace.trace_id
    )

    assert stored is not None
    assert len(
        stored.events
    ) == 3

    assert (
        stored.metrics.event_count
        == 3
    )


def test_stage_timing_collection():
    """
    Verify pipeline stage timing.
    """

    service = ContextObservabilityService()

    trace = service.start_trace()

    service.start_stage(
        trace.trace_id,
        "retrieval",
    )

    sleep(0.001)

    timing = service.complete_stage(
        trace.trace_id,
        "retrieval",
    )

    assert timing is not None
    assert timing.completed_at is not None
    assert timing.latency_ms >= 0

    stored = service.get_trace(
        trace.trace_id
    )

    assert stored.metrics.total_stages == 1
    assert stored.metrics.completed_stages == 1


def test_metrics_pipeline_health():
    """
    Verify pipeline health calculation.
    """

    health = calculate_pipeline_health(
        total_stages=4,
        completed_stages=4,
        failed_stages=0,
    )

    assert health == 1.0


def test_observability_summary_contains_metrics():
    """
    Verify final summary exposes collected metrics.
    """

    service = ContextObservabilityService()

    trace = service.start_trace()

    service.update_metrics(
        trace.trace_id,
        retrieved_items=10,
        ranked_items=8,
        selected_items=5,
    )

    summary = service.finish_trace(
        trace.trace_id
    )

    assert summary.metrics.retrieved_items == 10
    assert summary.metrics.ranked_items == 8
    assert summary.metrics.selected_items == 5
    assert summary.metrics.event_count >= 2
