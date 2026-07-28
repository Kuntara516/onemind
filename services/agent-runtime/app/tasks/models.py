from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .status import TaskStatus


class AgentTask(BaseModel):
    """
    Represents one unit of work executed by OneMind Agent Runtime.

    AgentTask is the execution contract between:
    - Agent Runtime
    - Task Manager
    - Executor
    - Capability Manager
    """

    task_id: str = Field(
        ...,
        description="Unique identifier of the task execution instance",
    )

    agent_id: str = Field(
        ...,
        description="Identifier of the Agent responsible for execution",
    )

    intent: str = Field(
        ...,
        description="Execution objective",
    )

    input: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution input parameters",
    )

    required_capabilities: list[str] = Field(
        default_factory=list,
        description="Capabilities required to complete the task",
    )

    execution_context: dict[str, Any] = Field(
        default_factory=dict,
        description="Runtime execution metadata",
    )

    status: TaskStatus = Field(
        default=TaskStatus.CREATED,
        description="Current lifecycle state of the task",
    )

    result: dict[str, Any] | None = Field(
        default=None,
        description="Execution output result",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp",
    )

    completed_at: datetime | None = Field(
        default=None,
        description="Task completion timestamp",
    )