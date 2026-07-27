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
        context
    ) -> dict:

        message = task.get(
            "message",
            ""
        )

        return {
            "message": (
                f"OneMind received: {message}"
            ),
            "request_id": (
                context.request_id
                if context
                else None
            )
        }