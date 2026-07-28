from app.agents.base import BaseAgent


class DemoAgent(BaseAgent):

    name = "demo-agent"

    description = (
        "First demonstration agent "
        "for OneMind runtime"
    )

    async def execute(
        self,
        task: dict,
        context,
        capabilities
    ) -> dict:

        message = task.get(
            "message",
            ""
        )

        tool_result = await capabilities.execute(
            "echo",
            text=message
        )

        return {
            "message": message,
            "request_id": (
                context.request_id
                if context
                else None
            ),
            "tool_result": tool_result
        }
