from typing import Any

from pydantic import BaseModel, Field


class AgentInvocationResult(BaseModel):
    """
    Standard response returned from Agent invocation.
    """

    success: bool = Field(
        ...,
        description="Invocation execution status",
    )

    output: Any | None = Field(
        default=None,
        description="Agent execution output",
    )

    error: str | None = Field(
        default=None,
        description="Error message when invocation fails",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Execution metadata",
    )