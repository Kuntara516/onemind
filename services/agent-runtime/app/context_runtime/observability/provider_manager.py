"""
Context Runtime Observability Provider Manager

Runtime provider selection layer for Context Runtime
observability backends.

Sprint:
    S4-010-003 Provider Integration Layer

Provides:

    Context Runtime
            |
            v
    Provider Manager
            |
            +-- InMemory Observability Service
            |
            +-- OpenTelemetry Provider


Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from .interface import ContextObservabilityInterface
from .service import ContextObservabilityService
from .providers.otel import (
    OpenTelemetryObservabilityProvider,
)


class ObservabilityProviderManager:
    """
    Manage Context Runtime observability providers.

    Responsibilities:

    - Create default observability provider
    - Select backend implementation
    - Hide provider construction details

    Supported providers:

    - memory
    - otel
    """

    def __init__(
        self,
        provider: str = "memory",
    ) -> None:

        self.provider_name = provider

        self._provider = (
            self._create_provider(
                provider
            )
        )

    # -------------------------------------------------
    # Provider selection
    # -------------------------------------------------

    def get_provider(
        self,
    ) -> ContextObservabilityInterface:
        """
        Return active observability provider.

        Note:

        OpenTelemetry provider currently
        exposes telemetry primitives while
        ContextObservabilityService remains
        the primary lifecycle provider.
        """

        return self._provider


    # -------------------------------------------------
    # Factory
    # -------------------------------------------------

    def _create_provider(
        self,
        provider: str,
    ):
        """
        Create provider implementation.
        """

        if provider == "memory":

            return ContextObservabilityService()


        if provider == "otel":

            return OpenTelemetryObservabilityProvider()


        raise ValueError(
            f"Unsupported observability provider: {provider}"
        )
