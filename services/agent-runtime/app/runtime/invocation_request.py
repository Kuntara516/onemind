from pydantic import BaseModel, ConfigDict, Field

from app.tasks.models import AgentTask
from app.agents.context import AgentContext


class AgentInvocationRequest(BaseModel):
    """
    Request contract for invoking an Agent.
    """

    agent_id: str = Field(
        ...,
        description="Target agent identifier",
    )

    task: AgentTask = Field(
        ...,
        description="Task assigned to agent",
    )

    context: AgentContext = Field(
        ...,
        description="Runtime execution context",
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )