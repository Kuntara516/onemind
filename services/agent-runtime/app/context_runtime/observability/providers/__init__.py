"""
Context Runtime Observability Providers

Sprint:
    S4-010-002 OpenTelemetry Trace Provider

Provider implementations for Context Runtime
observability backends.
"""

from .otel import (
    OpenTelemetryObservabilityProvider,
    OTEL_AVAILABLE,
)


__all__ = [
    "OpenTelemetryObservabilityProvider",
    "OTEL_AVAILABLE",
]
