"""
OpenTelemetry Context Runtime Provider

Sprint:
    S4-010-002 OpenTelemetry Trace Provider

Provides OpenTelemetry-compatible tracing backend
for Context Runtime observability.

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


try:
    from opentelemetry import trace

    OTEL_AVAILABLE = True

except ImportError:
    trace = None
    OTEL_AVAILABLE = False


class OpenTelemetryObservabilityProvider:
    """
    OpenTelemetry provider for Context Runtime.

    Responsibilities:

    - create runtime traces
    - create stage spans
    - attach telemetry attributes
    - gracefully fallback without OTEL SDK
    """

    def __init__(
        self,
        service_name: str = "onemind-context-runtime",
    ) -> None:

        self.service_name = service_name

        if OTEL_AVAILABLE:
            self.tracer = trace.get_tracer(
                service_name
            )
        else:
            self.tracer = None


    # -------------------------------------------------
    # Trace lifecycle
    # -------------------------------------------------

    def start_trace(
        self,
        *,
        name: str = "context_runtime",
        attributes: dict[str, Any] | None = None,
    ):
        """
        Start context runtime trace.
        """

        if self.tracer:

            span = self.tracer.start_span(
                name
            )

            self._set_attributes(
                span,
                attributes,
            )

            return span


        return {
            "name": name,
            "started_at": datetime.now(UTC),
            "attributes": attributes or {},
        }


    def end_trace(
        self,
        span,
        *,
        success: bool = True,
    ) -> None:
        """
        Finish trace.
        """

        if hasattr(
            span,
            "set_attribute",
        ):

            span.set_attribute(
                "context.runtime.success",
                success,
            )

        if hasattr(
            span,
            "end",
        ):

            span.end()


    # -------------------------------------------------
    # Stage lifecycle
    # -------------------------------------------------

    def start_stage(
        self,
        stage: str,
    ):
        """
        Start pipeline stage.
        """

        if self.tracer:

            return self.tracer.start_span(
                f"context.{stage}"
            )


        return {
            "stage": stage,
            "started_at": datetime.now(UTC),
        }


    def end_stage(
        self,
        span,
        *,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """
        Finish pipeline stage.
        """

        self._set_attributes(
            span,
            attributes,
        )

        if hasattr(
            span,
            "end",
        ):

            span.end()


    # -------------------------------------------------
    # Internal helpers
    # -------------------------------------------------

    @staticmethod
    def _set_attributes(
        span,
        attributes: dict[str, Any] | None,
    ) -> None:
        """
        Attach OpenTelemetry attributes safely.
        """

        if not attributes:
            return


        if not hasattr(
            span,
            "set_attribute",
        ):
            return


        for key, value in attributes.items():

            span.set_attribute(
                key,
                value,
            )
