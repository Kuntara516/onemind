from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """
    Execution runtime event types.

    Events represent state transitions
    during Agent Runtime execution.
    """

    EXECUTION_STARTED = "execution.started"
    EXECUTION_FINISHED = "execution.finished"

    AGENT_SELECTED = "agent.selected"
    AGENT_STARTED = "agent.started"
    AGENT_FINISHED = "agent.finished"

    CAPABILITY_STARTED = "capability.started"
    CAPABILITY_FINISHED = "capability.finished"

    LLM_STARTED = "llm.started"
    LLM_FINISHED = "llm.finished"

    ERROR = "error"


class ExecutionEvent(BaseModel):
    """
    Represents one runtime execution event.
    """

    event_id: str = Field(
        ...,
        description="Unique identifier of execution event",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Event creation timestamp",
    )

    request_id: str = Field(
        ...,
        description="Request identifier associated with execution",
    )

    task_id: str = Field(
        ...,
        description="Task identifier associated with execution",
    )

    event_type: EventType = Field(
        ...,
        description="Execution event type",
    )

    agent: str | None = Field(
        default=None,
        description="Agent involved in execution event",
    )

    message: str | None = Field(
        default=None,
        description="Human readable event message",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional event metadata",
    )