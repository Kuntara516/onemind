"""
Context Runtime Observability Tests

Sprint:
S4-009 Context Runtime Observability
S4-010-005 Observability Validation & Runtime Metrics

Coverage:

- Trace lifecycle
- Event tracking
- Stage timing
- Metrics collection
- Runtime metrics validation
- Runtime adapter integration
- Provider boundary
- Public observability access only
- Runtime/provider isolation

Author:
OneMind Platform

License:
MIT
"""

from __future__ import annotations

from inspect import getsource
from time import sleep

from app.context_runtime.observability import (
    ContextObservabilityService,
    ContextRuntimeEvent,
    ContextRuntimeObservabilityRuntime,
)
from app.context_runtime.observability.metrics import (
    calculate_pipeline_health,
    calculate_selection_ratio,
)


# ---------------------------------------------------------------------------
# Trace lifecycle
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Event tracking
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Stage timing
# ---------------------------------------------------------------------------


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

    assert (
        stored.metrics.total_stages
        == 1
    )

    assert (
        stored.metrics.completed_stages
        == 1
    )


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


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

    assert (
        summary.metrics.retrieved_items
        == 10
    )

    assert (
        summary.metrics.ranked_items
        == 8
    )

    assert (
        summary.metrics.selected_items
        == 5
    )

    assert (
        summary.metrics.event_count
        >= 2
    )


def test_selection_ratio_calculation():
    """
    Verify context selection ratio metric.
    """

    ratio = calculate_selection_ratio(
        retrieved_items=10,
        selected_items=5,
    )

    assert ratio == 0.5


def test_compression_metrics_collection():
    """
    Verify compression metrics are stored in snapshot.
    """

    service = ContextObservabilityService()

    trace = service.start_trace()

    service.update_metrics(
        trace.trace_id,
        original_tokens=1000,
        compressed_tokens=400,
    )

    summary = service.finish_trace(
        trace.trace_id
    )

    assert (
        summary.metrics.original_tokens
        == 1000
    )

    assert (
        summary.metrics.compressed_tokens
        == 400
    )

    assert (
        summary.metrics.compression_ratio
        == 0.4
    )

    assert (
        summary.metrics.token_reduction
        == 600
    )


# ---------------------------------------------------------------------------
# Runtime observability adapter
# ---------------------------------------------------------------------------


def test_runtime_observability_adapter_lifecycle():
    """
    Verify runtime adapter delegates lifecycle
    through the observability provider layer.
    """

    runtime = ContextRuntimeObservabilityRuntime()

    trace = runtime.start_trace(
        "execution-001",
    )

    assert trace is not None

    runtime.record_event(
        "execution-001",
        ContextRuntimeEvent.CONTEXT_BUILD_STARTED,
    )

    runtime.finish_trace(
        "execution-001",
    )


# ---------------------------------------------------------------------------
# Boundary validation
# ---------------------------------------------------------------------------


def test_runtime_observability_exposes_public_lifecycle_only():
    """
    Verify the runtime adapter is exercised through
    its public lifecycle methods rather than private
    provider state.
    """

    runtime = ContextRuntimeObservabilityRuntime()

    assert callable(
        runtime.start_trace
    )

    assert callable(
        runtime.record_event
    )

    assert callable(
        runtime.finish_trace
    )


def test_runtime_adapter_does_not_require_private_trace_store():
    """
    Verify consumers do not need direct access to
    the provider's private trace registry.

    The private trace store belongs to the provider
    implementation and must not be part of the
    runtime integration contract.
    """

    runtime = ContextRuntimeObservabilityRuntime()

    public_methods = {
        "start_trace",
        "record_event",
        "finish_trace",
    }

    for method_name in public_methods:
        assert hasattr(
            runtime,
            method_name,
        )

    assert not hasattr(
        runtime,
        "_active_traces",
    )


def test_runtime_observability_boundary_has_no_private_provider_access():
    """
    Verify the runtime adapter implementation does not
    depend on the provider's private trace registry.
    """

    source = getsource(
        ContextRuntimeObservabilityRuntime
    )

    assert "_active_traces" not in source
    assert "observability.provider" not in source


def test_observability_service_private_trace_store_is_provider_internal():
    """
    Verify the in-memory trace registry remains private
    to the provider implementation.
    """

    service = ContextObservabilityService()

    assert hasattr(
        service,
        "_traces",
    )

    assert not hasattr(
        service,
        "active_traces",
    )


def test_runtime_adapter_isolated_from_direct_provider_usage():
    """
    Verify the runtime adapter can operate through its
    public API without consumers constructing or managing
    ContextObservabilityService directly.
    """

    runtime = ContextRuntimeObservabilityRuntime()

    trace = runtime.start_trace(
        "boundary-execution-001",
    )

    assert trace is not None

    runtime.record_event(
        "boundary-execution-001",
        ContextRuntimeEvent.RETRIEVAL_STARTED,
    )

    summary = runtime.finish_trace(
        "boundary-execution-001",
    )

    assert summary is not None
    assert summary.success is True
