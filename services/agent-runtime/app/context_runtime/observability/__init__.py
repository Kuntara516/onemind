"""
Context Runtime Observability Package

Public API exports for S4-010
Context Runtime Observability.

Provides:

    Context Runtime
            |
            v
    Observability Interface
            |
            +-- ContextObservabilityService
            |
            +-- ObservabilityProviderManager
            |
            +-- OpenTelemetry Provider


Sprint:
    S4-009 Context Runtime Observability
    S4-010 Provider Integration Layer

Author:
    OneMind Platform

License:
    MIT
"""

from .events import ContextRuntimeEvent

from .models import (
    ContextMetricsSnapshot,
    ContextRuntimeSummary,
    ContextRuntimeTrace,
    ContextStageTiming,
    ContextTraceEvent,
)

from .interface import (
    ContextObservabilityInterface,
)

from .service import (
    ContextObservabilityService,
)

from .provider_manager import (
    ObservabilityProviderManager,
)

from .providers import (
    OpenTelemetryObservabilityProvider,
    OTEL_AVAILABLE,
)


__all__ = [
    "ContextRuntimeEvent",
    "ContextMetricsSnapshot",
    "ContextRuntimeSummary",
    "ContextRuntimeTrace",
    "ContextStageTiming",
    "ContextTraceEvent",
    "ContextObservabilityInterface",
    "ContextObservabilityService",
    "ObservabilityProviderManager",
    "OpenTelemetryObservabilityProvider",
    "OTEL_AVAILABLE",
]
