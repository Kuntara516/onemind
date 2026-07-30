from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from .event import (
    ExecutionEvent,
    EventType,
)


class ExecutionTrace(BaseModel):
    """
    Represents one complete Agent Runtime execution lifecycle.

    ExecutionTrace collects runtime events
    and preserves execution history.
    """

    trace_id: str = Field(
        default_factory=lambda: str(uuid4()),
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
        event_type: str,
        message: str | None = None,
        metadata: dict | None = None,
    ):
        """
        Create and append execution event.
        """

        event = ExecutionEvent(
            event_id=str(uuid4()),
            request_id=self.request_id,
            task_id=self.task_id,
            event_type=EventType(event_type),
            message=message,
            metadata=metadata or {},
        )

        self.events.append(
            event
        )


    def finish(self):
        """
        Mark execution trace as completed.
        """

        self.finished_at = datetime.now(
            timezone.utc
        )


    def to_dict(self):
        """
        Serialize execution trace.
        """

        return self.model_dump()