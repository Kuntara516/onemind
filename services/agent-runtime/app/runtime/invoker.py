from app.registry import AgentRegistry
from app.capability_manager import CapabilityManager

from app.runtime.invocation_request import (
    AgentInvocationRequest,
)

from app.runtime.invocation_result import (
    AgentInvocationResult,
)


class AgentInvoker:
    """
    Responsible for invoking OneMind agents.

    Boundary between:
    Executor
        |
        v
    Agent Runtime
        |
        v
    Agent implementation
    """

    def __init__(
        self,
        registry: AgentRegistry,
        capability_manager: CapabilityManager,
    ):
        self.registry = registry
        self.capability_manager = capability_manager


    async def invoke(
        self,
        request: AgentInvocationRequest,
    ) -> AgentInvocationResult:
        """
        Invoke agent execution.
        """

        agent = self.registry.get(
            request.agent_id
        )

        if agent is None:
            return AgentInvocationResult(
                success=False,
                error=(
                    f"Agent not found: "
                    f"{request.agent_id}"
                ),
            )


        try:
            output = await agent.execute(
                request.task.input,
                request.context,
                self.capability_manager,
            )

            return AgentInvocationResult(
                success=True,
                output=output,
                metadata={
                    "agent_id": request.agent_id,
                    "task_id": request.task.task_id,
                },
            )

        except Exception as exc:
            return AgentInvocationResult(
                success=False,
                error=str(exc),
                metadata={
                    "agent_id": request.agent_id,
                    "task_id": request.task.task_id,
                },
            )