"""
Context Runtime Observability Provider Interface

Defines the abstraction boundary between
Context Runtime Observability Service and
external telemetry providers.

Sprint:
    S4-010-003 Observability Provider Integration

Implementations:

    Provider Interface
            |
            +-- OpenTelemetry Provider
            |
            +-- Prometheus Provider
            |
            +-- Logging Provider

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ObservabilityProviderInterface(ABC):
    """
    Abstract contract for telemetry providers.

    This interface intentionally does not expose
    internal Context Runtime models.

    It only manages external tracing lifecycle.
    """

    # -------------------------------------------------
    # Trace lifecycle
    # -------------------------------------------------

    @abstractmethod
    def start_trace(
        self,
        *,
        name: str = "context_runtime",
        attributes: dict[str, Any] | None = None,
    ):
        """
        Start external trace/span.
        """
        raise NotImplementedError


    @abstractmethod
    def end_trace(
        self,
        span,
        *,
        success: bool = True,
    ) -> None:
        """
        Finish external trace/span.
        """
        raise NotImplementedError


    # -------------------------------------------------
    # Stage lifecycle
    # -------------------------------------------------

    @abstractmethod
    def start_stage(
        self,
        stage: str,
    ):
        """
        Start external stage span.
        """
        raise NotImplementedError


    @abstractmethod
    def end_stage(
        self,
        span,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """
        Finish external stage span.
        """
        raise NotImplementedError
