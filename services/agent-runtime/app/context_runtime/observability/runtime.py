"""
Context Runtime Observability Runtime Adapter

Bridges Context Runtime execution lifecycle
with observability providers.

Sprint:
    S4-010-004 Observability Runtime Integration

Responsibilities:

- create runtime traces
- manage active execution traces
- emit lifecycle events
- track pipeline stages
- finalize execution telemetry

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

        self._active_traces: dict[
            str,
            Any,
        ] = {}

        self._active_stages: dict[
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
        Start execution trace.

        Supports:

        ContextObservabilityService:
            start_trace(
                request_id=,
                metadata=
            )

        OpenTelemetry provider:
            start_trace(
                name=,
                attributes=
            )
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

        self._active_traces[
            execution_id
        ] = trace

        return trace

    def finish_trace(
        self,
        execution_id: str,
        *,
        success: bool = True,
    ) -> None:
        """
        Finish execution trace.
        """

        trace = self._active_traces.pop(
            execution_id,
            None,
        )

        if trace is None:
            return

        if hasattr(
            self.provider,
            "end_trace",
        ):

            self.provider.end_trace(
                trace,
                success=success,
            )

            return

        if hasattr(
            self.provider,
            "finish_trace",
        ):

            trace_id = getattr(
                trace,
                "trace_id",
                None,
            )

            if trace_id is not None:

                self.provider.finish_trace(
                    trace_id,
                    success=success,
                )

    # ---------------------------------------------------------
    # Events
    # ---------------------------------------------------------

    def record_event(
        self,
        execution_id: str,
        event: ContextRuntimeEvent,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """
        Record runtime lifecycle event.
        """

        trace = self._active_traces.get(
            execution_id
        )

        if trace is None:
            return

        trace_id = getattr(
            trace,
            "trace_id",
            None,
        )

        if hasattr(
            self.provider,
            "record_event",
        ) and trace_id is not None:

            self.provider.record_event(
                trace_id,
                event,
                metadata=attributes,
            )

            return

        if hasattr(
            trace,
            "add_event",
        ):

            trace.add_event(
                event.value,
                attributes or {},
            )

    # ---------------------------------------------------------
    # Stage lifecycle
    # ---------------------------------------------------------

    def _get_trace_id(
        self,
        execution_id: str,
    ):
        """
        Resolve provider trace identifier.

        Memory provider uses UUID trace_id.
        OpenTelemetry provider uses span object.
        """

        trace = self._active_traces.get(
            execution_id
        )

        if trace is None:
            return None

        return getattr(
            trace,
            "trace_id",
            trace,
        )

    def start_stage(
        self,
        execution_id: str,
        stage: str,
    ) -> Any:
        """
        Start context pipeline stage.
        """

        trace_id = self._get_trace_id(
            execution_id
        )

        if hasattr(
            self.provider,
            "start_stage",
        ):

            try:

                span = self.provider.start_stage(
                    trace_id,
                    stage,
                )

            except TypeError:

                span = self.provider.start_stage(
                    stage,
                )

        else:

            span = None

        self._active_stages[
            f"{execution_id}:{stage}"
        ] = span

        return span

    def finish_stage(
        self,
        execution_id: str,
        stage: str,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """
        Finish context pipeline stage.
        """

        key = (
            f"{execution_id}:{stage}"
        )

        span = self._active_stages.pop(
            key,
            None,
        )

        if span is None:
            return

        if hasattr(
            self.provider,
            "end_stage",
        ):

            self.provider.end_stage(
                span,
                attributes=attributes,
            )

            return

        if hasattr(
            self.provider,
            "complete_stage",
        ):

            trace_id = self._get_trace_id(
                execution_id
            )

            self.provider.complete_stage(
                trace_id,
                stage,
            )

    # ---------------------------------------------------------
    # Context runtime lifecycle helpers
    # ---------------------------------------------------------

    def context_build_started(
        self,
        execution_id: str,
    ) -> None:
        """
        Emit context build started event.
        """

        self.record_event(
            execution_id,
            ContextRuntimeEvent.CONTEXT_BUILD_STARTED,
        )

    def context_finished(
        self,
        execution_id: str,
        *,
        success: bool = True,
    ) -> None:
        """
        Complete context runtime execution.
        """

        self.record_event(
            execution_id,
            (
                ContextRuntimeEvent.FINISHED
                if success
                else ContextRuntimeEvent.FAILED
            ),
        )

        self.finish_trace(
            execution_id,
            success=success,
        )
