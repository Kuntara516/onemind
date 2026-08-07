"""
Context Runtime Observability Interface

Defines the abstraction boundary between
Context Runtime execution and observability providers.

Sprint:
    S4-010-001 Observability Interface Foundation

The interface allows different observability backends:

    Context Runtime
            |
            v
    Observability Interface
            |
            +-- InMemory Provider
            |
            +-- OpenTelemetry Provider
            |
            +-- External Telemetry Systems


Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from .events import ContextRuntimeEvent
from .models import (
    ContextRuntimeSummary,
    ContextRuntimeTrace,
    ContextStageTiming,
    ContextTraceEvent,
)


class ContextObservabilityInterface(ABC):
    """
    Abstract observability contract.

    Context Runtime should depend on this interface
    instead of a concrete implementation.
    """

    # --------------------------------------------------------------
    # Trace lifecycle
    # --------------------------------------------------------------

    @abstractmethod
    def start_trace(
        self,
        *,
        request_id: str | None = None,
        task_id: str | None = None,
        agent_id: str | None = None,
        metadata: dict | None = None,
    ) -> ContextRuntimeTrace:
        """
        Start a new runtime trace.
        """
        raise NotImplementedError

    @abstractmethod
    def finish_trace(
        self,
        trace_id: UUID,
        *,
        success: bool = True,
    ) -> ContextRuntimeSummary:
        """
        Finish runtime trace.
        """
        raise NotImplementedError

    @abstractmethod
    def get_trace(
        self,
        trace_id: UUID,
    ) -> ContextRuntimeTrace | None:
        """
        Retrieve trace.
        """
        raise NotImplementedError

    # --------------------------------------------------------------
    # Events
    # --------------------------------------------------------------

    @abstractmethod
    def record_event(
        self,
        trace_id: UUID,
        event: ContextRuntimeEvent,
        *,
        metadata: dict | None = None,
    ) -> ContextTraceEvent:
        """
        Record runtime event.
        """
        raise NotImplementedError

    # --------------------------------------------------------------
    # Stage timing
    # --------------------------------------------------------------

    @abstractmethod
    def start_stage(
        self,
        trace_id: UUID,
        stage: str,
    ) -> ContextStageTiming:
        """
        Start stage timer.
        """
        raise NotImplementedError

    @abstractmethod
    def complete_stage(
        self,
        trace_id: UUID,
        stage: str,
    ) -> ContextStageTiming | None:
        """
        Complete stage timer.
        """
        raise NotImplementedError

    # --------------------------------------------------------------
    # Metrics
    # --------------------------------------------------------------

    @abstractmethod
    def update_metrics(
        self,
        trace_id: UUID,
        *,
        retrieved_items: int = 0,
        ranked_items: int = 0,
        selected_items: int = 0,
        original_tokens: int = 0,
        compressed_tokens: int = 0,
    ) -> None:
        """
        Update runtime metrics.
        """
        raise NotImplementedError
