from pydantic import BaseModel, Field

from app.tasks.models import AgentTask
from app.agents.context import AgentContext


class AgentInvocationRequest(BaseModel):
    """
    Request contract for invoking an Agent.

    Flow:

    Executor
        |
        v
    AgentInvoker
        |
        v
    Agent Runtime
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