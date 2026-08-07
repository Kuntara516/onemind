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
            +-- ContextRuntimeObservabilityRuntime
            |
            +-- ObservabilityProviderManager
            |
            +-- OpenTelemetry Provider


Sprint:
    S4-009 Context Runtime Observability
    S4-010 Provider Integration Layer
    S4-010-005 Observability Validation & Runtime Metrics

Author:
    OneMind Platform

License:
    MIT
"""

from .events import (
    ContextRuntimeEvent,
)

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

from .runtime import (
    ContextRuntimeObservabilityRuntime,
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
    "ContextRuntimeObservabilityRuntime",
    "ObservabilityProviderManager",
    "OpenTelemetryObservabilityProvider",
    "OTEL_AVAILABLE",
]
