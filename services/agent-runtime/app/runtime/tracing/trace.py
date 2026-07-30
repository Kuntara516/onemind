from datetime import datetime, timezone

from pydantic import BaseModel, Field

from .event import ExecutionEvent


class ExecutionTrace(BaseModel):
    """
    Represents one complete Agent Runtime execution lifecycle.

    ExecutionTrace collects runtime events
    and preserves execution history.
    """

    trace_id: str = Field(
        ...,
        description="Unique identifier of execution trace",
    )

    request_id: str = Field(
        ...,
        description="Request identifier associated with execution",
    )

    task_id: str = Field(
        ...,
        description="Task identifier associated with execution",
    )

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Trace start timestamp",
    )

    finished_at: datetime | None = Field(
        default=None,
        description="Trace completion timestamp",
    )

    events: list[ExecutionEvent] = Field(
        default_factory=list,
        description="Ordered execution event history",
    )

    def add_event(
        self,
        event: ExecutionEvent,
    ):
        """
        Add an execution event to trace history.
        """

        self.events.append(event)

    def finish(self):
        """
        Mark execution trace as completed.
        """

        self.finished_at = datetime.now(timezone.utc)

    def to_dict(self):
        """
        Serialize execution trace.

        Returns:
            dict representation of trace.
        """

        return self.model_dump()