from app.registry import registry


class AgentRuntime:

    async def execute(self, agent_name: str, task: dict):

        agent = registry.get(agent_name)

        if not agent:
            return {
                "status": "error",
                "message": f"Agent {agent_name} not found"
            }

        result = await agent.execute(task)

        return {
            "status": "completed",
            "agent": agent_name,
            "result": result
        }


runtime = AgentRuntime()