"""
Context Runtime Observability Events

Defines lifecycle events emitted by the Context Runtime pipeline.
These events are consumed by the ContextObservabilityService to
build execution traces and metrics.

Sprint:
    S4-009 Context Runtime Observability

Author:
    OneMind Platform

License:
    MIT
"""

from enum import Enum


class ContextRuntimeEvent(str, Enum):
    """
    Lifecycle events for Context Runtime execution.

    These events represent the major phases of context processing.
    """

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    RETRIEVAL_STARTED = "retrieval_started"
    RETRIEVAL_COMPLETED = "retrieval_completed"

    # ------------------------------------------------------------------
    # Ranking
    # ------------------------------------------------------------------

    RANKING_STARTED = "ranking_started"
    RANKING_COMPLETED = "ranking_completed"

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    SELECTION_STARTED = "selection_started"
    SELECTION_COMPLETED = "selection_completed"

    # ------------------------------------------------------------------
    # Compression
    # ------------------------------------------------------------------

    COMPRESSION_STARTED = "compression_started"
    COMPRESSION_COMPLETED = "compression_completed"

    # ------------------------------------------------------------------
    # Assembly
    # ------------------------------------------------------------------

    ASSEMBLY_STARTED = "assembly_started"
    ASSEMBLY_COMPLETED = "assembly_completed"

    # ------------------------------------------------------------------
    # Runtime lifecycle
    # ------------------------------------------------------------------

    CONTEXT_BUILD_STARTED = "context_build_started"
    CONTEXT_BUILD_COMPLETED = "context_build_completed"

    FINISHED = "finished"
    FAILED = "failed"

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    @property
    def is_start_event(self) -> bool:
        """Return True if this event marks the start of a stage."""
        return self.value.endswith("_started")

    @property
    def is_completion_event(self) -> bool:
        """Return True if this event marks the successful completion of a stage."""
        return self.value.endswith("_completed")

    @property
    def is_terminal_event(self) -> bool:
        """Return True if this event terminates the execution trace."""
        return self in {
            ContextRuntimeEvent.FINISHED,
            ContextRuntimeEvent.FAILED,
        }

    @property
    def stage(self) -> str:
        """
        Return the logical pipeline stage for this event.

        Examples:
            RETRIEVAL_STARTED -> "retrieval"
            COMPRESSION_COMPLETED -> "compression"
            FINISHED -> "runtime"
        """
        mapping = {
            ContextRuntimeEvent.RETRIEVAL_STARTED: "retrieval",
            ContextRuntimeEvent.RETRIEVAL_COMPLETED: "retrieval",

            ContextRuntimeEvent.RANKING_STARTED: "ranking",
            ContextRuntimeEvent.RANKING_COMPLETED: "ranking",

            ContextRuntimeEvent.SELECTION_STARTED: "selection",
            ContextRuntimeEvent.SELECTION_COMPLETED: "selection",

            ContextRuntimeEvent.COMPRESSION_STARTED: "compression",
            ContextRuntimeEvent.COMPRESSION_COMPLETED: "compression",

            ContextRuntimeEvent.ASSEMBLY_STARTED: "assembly",
            ContextRuntimeEvent.ASSEMBLY_COMPLETED: "assembly",

            ContextRuntimeEvent.CONTEXT_BUILD_STARTED: "context_build",
            ContextRuntimeEvent.CONTEXT_BUILD_COMPLETED: "context_build",

            ContextRuntimeEvent.FINISHED: "runtime",
            ContextRuntimeEvent.FAILED: "runtime",
        }

        return mapping[self]

    def __str__(self) -> str:
        """Return the string representation of the event."""
        return self.value
