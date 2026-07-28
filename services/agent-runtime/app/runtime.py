from uuid import uuid4

from app.registry import registry
from app.agents.context import AgentContext


class AgentRuntime:
    """
    Core execution engine for OneMind agents.

    Responsible for:
    - Agent resolution
    - Context creation
    - Execution lifecycle
    - Result metadata collection
    """

    async def execute(
        self,
        agent_name: str,
        capability_manager,
        task: dict
    ):

        # -------------------------------------------------
        # Resolve Agent
        # -------------------------------------------------

        agent = registry.get(agent_name)

        if not agent:
            return {
                "status": "error",
                "message": (
                    f"Agent {agent_name} not found"
                )
            }


        # -------------------------------------------------
        # Create Execution Context
        # -------------------------------------------------

        context = AgentContext(
            request_id=str(uuid4())
        )


        # -------------------------------------------------
        # Execute Agent
        # -------------------------------------------------

        try:

            result = await agent.execute(
                task,
                context,
                capability_manager
            )

            return {
                "status": "completed",
                "agent": agent_name,
                "request_id": context.request_id,
                "context": {
                    "session_id": context.session_id,
                    "user_id": context.user_id
                },
                "result": result
            }


        except Exception as error:

            return {
                "status": "failed",
                "agent": agent_name,
                "request_id": context.request_id,
                "error": str(error)
            }


runtime = AgentRuntime()
