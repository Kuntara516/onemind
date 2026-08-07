"""
Context Runtime Observability Providers

Provider implementations for Context Runtime
observability backends.

Sprint:
    S4-010-002 OpenTelemetry Trace Provider

Provides:

    Context Runtime
            |
            v
    Observability Provider Layer
            |
            +-- OpenTelemetry Provider


Author:
    OneMind Platform

License:
    MIT
"""

from .otel import (
    OpenTelemetryObservabilityProvider,
    OTEL_AVAILABLE,
)


__all__ = [
    "OpenTelemetryObservabilityProvider",
    "OTEL_AVAILABLE",
]
