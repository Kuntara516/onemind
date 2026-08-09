"""
Context Runtime Observability Runtime Adapter

Bridges Context Runtime execution lifecycle
with observability providers.

Sprint:
S4-010-004 Observability Runtime Integration

Responsibilities:

- create runtime traces
- emit lifecycle events
- track pipeline stages
- update runtime metrics
- finalize execution telemetry
- isolate Context Runtime from provider internals

The adapter intentionally owns only opaque execution handles.
It does not access provider-private state.

Supports:

- ContextObservabilityService
- OpenTelemetryObservabilityProvider

Author:
OneMind Platform

License:
MIT
"""

from __future__ import annotations

from typing import Any

from .events import ContextRuntimeEvent
from .provider_manager import ObservabilityProviderManager


class ContextRuntimeObservabilityRuntime:
    """
    Runtime integration layer for observability.

    This adapter isolates Context Runtime execution
    from concrete observability implementations.

    Architecture:

        Context Runtime
              |
              v
        Observability Runtime Adapter
              |
              v
        Observability Provider Manager
              |
              +----------------------+
              |                      |
              v                      v
    ContextObservabilityService   OpenTelemetry Provider

    The runtime adapter stores only opaque provider
    handles associated with execution IDs.

    It must never access provider-private registries
    such as ``_traces``.
    """

    def __init__(
        self,
        provider_manager: ObservabilityProviderManager | None = None,
    ) -> None:
        self.provider_manager = (
            provider_manager
            or ObservabilityProviderManager()
        )

        self.provider = (
            self.provider_manager.get_provider()
        )

        # Opaque provider handles keyed by Context Runtime
        # execution ID. The adapter does not inspect provider
        # private storage.
        self._execution_traces: dict[
            str,
            Any,
        ] = {}

        self._execution_stages: dict[
            str,
            Any,
        ] = {}

    # ---------------------------------------------------------
    # Trace lifecycle
    # ---------------------------------------------------------

    def start_trace(
        self,
        execution_id: str,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> Any:
        """
        Start an execution trace.

        The provider-specific construction details remain
        behind the provider boundary.
        """

        metadata = {
            "context.runtime.execution_id": execution_id,
            **(attributes or {}),
        }

        try:
            trace = self.provider.start_trace(
                request_id=execution_id,
                metadata=metadata,
            )
        except TypeError:
            trace = self.provider.start_trace(
                name="context_runtime_execution",
                attributes=metadata,
            )

        self._execution_traces[
            execution_id
        ] = trace

        return trace

    def finish_trace(
        self,
        execution_id: str,
        *,
        success: bool = True,
    ) -> Any:
        """
        Finish an execution trace.

        Returns the provider's completion result when the
        provider exposes a Context Runtime summary.

        External telemetry providers that only expose an
        ``end_trace`` operation return ``None``.
        """

        trace = self._execution_traces.pop(
            execution_id,
            None,
        )

        if trace is None:
            return None

        # ContextObservabilityService boundary.
        finish_trace = getattr(
            self.provider,
            "finish_trace",
            None,
        )

        if callable(finish_trace):
            trace_id = getattr(
                trace,
                "trace_id",
                None,
            )

            if trace_id is None:
                return None

            return finish_trace(
                trace_id,
                success=success,
            )

        # External telemetry provider boundary.
        end_trace = getattr(
            self.provider,
            "end_trace",
            None,
        )

        if callable(end_trace):
            end_trace(
                trace,
                success=success,
            )

        return None

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------

    def record_event(
        self,
        execution_id: str,
        event: ContextRuntimeEvent,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> Any:
        """
        Record a runtime lifecycle event.

        The adapter resolves the opaque execution handle
        and delegates through the provider's public API.
        """

        trace = self._execution_traces.get(
            execution_id
        )

        if trace is None:
            return None

        trace_id = getattr(
            trace,
            "trace_id",
            None,
        )

        record_event = getattr(
            self.provider,
            "record_event",
            None,
        )

        if callable(record_event) and trace_id is not None:
            return record_event(
                trace_id,
                event,
                metadata=attributes,
            )

        add_event = getattr(
            trace,
            "add_event",
            None,
        )

        if callable(add_event):
            return add_event(
                event.value,
                attributes or {},
            )

        return None

    # ---------------------------------------------------------
    # Stage lifecycle
    # ---------------------------------------------------------

    def start_stage(
        self,
        execution_id: str,
        stage: str,
    ) -> Any:
        """
        Start a context pipeline stage.

        Provider-specific stage handles are stored as
        opaque values by the adapter.
        """

        trace = self._execution_traces.get(
            execution_id
        )

        if trace is None:
            return None

        trace_id = getattr(
            trace,
            "trace_id",
            trace,
        )

        start_stage = getattr(
            self.provider,
            "start_stage",
            None,
        )

        if not callable(start_stage):
            return None

        try:
            stage_handle = start_stage(
                trace_id,
                stage,
            )
        except TypeError:
            stage_handle = start_stage(
                stage,
            )

        self._execution_stages[
            f"{execution_id}:{stage}"
        ] = stage_handle

        return stage_handle

    def finish_stage(
        self,
        execution_id: str,
        stage: str,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> Any:
        """
        Finish a context pipeline stage.
        """

        key = (
            f"{execution_id}:{stage}"
        )

        stage_handle = self._execution_stages.pop(
            key,
            None,
        )

        if stage_handle is None:
            return None

        end_stage = getattr(
            self.provider,
            "end_stage",
            None,
        )

        if callable(end_stage):
            return end_stage(
                stage_handle,
                attributes=attributes,
            )

        complete_stage = getattr(
            self.provider,
            "complete_stage",
            None,
        )

        if callable(complete_stage):
            trace = self._execution_traces.get(
                execution_id
            )

            if trace is None:
                return None

            trace_id = getattr(
                trace,
                "trace_id",
                trace,
            )

            return complete_stage(
                trace_id,
                stage,
            )

        return None

    # ---------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------

    def update_metrics(
        self,
        execution_id: str,
        *,
        retrieved_items: int = 0,
        ranked_items: int = 0,
        selected_items: int = 0,
        original_tokens: int = 0,
        compressed_tokens: int = 0,
    ) -> Any:
        """
        Update metrics for an active runtime trace.

        The Context Runtime integration layer must use this
        method instead of accessing provider state directly.
        """

        trace = self._execution_traces.get(
            execution_id
        )

        if trace is None:
            return None

        trace_id = getattr(
            trace,
            "trace_id",
            None,
        )

        if trace_id is None:
            return None

        update_metrics = getattr(
            self.provider,
            "update_metrics",
            None,
        )

        if not callable(update_metrics):
            return None

        return update_metrics(
            trace_id,
            retrieved_items=retrieved_items,
            ranked_items=ranked_items,
            selected_items=selected_items,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
        )

    # ---------------------------------------------------------
    # Context runtime lifecycle helpers
    # ---------------------------------------------------------

    def context_build_started(
        self,
        execution_id: str,
    ) -> Any:
        """
        Emit context build started event.
        """

        return self.record_event(
            execution_id,
            ContextRuntimeEvent.CONTEXT_BUILD_STARTED,
        )

    def context_finished(
        self,
        execution_id: str,
        *,
        success: bool = True,
    ) -> Any:
        """
        Complete context runtime execution.

        ``finish_trace`` owns terminal event emission.
        This helper therefore delegates directly to it
        to guarantee exactly one FINISHED or FAILED event.
        """

        return self.finish_trace(
            execution_id,
            success=success,
        )
