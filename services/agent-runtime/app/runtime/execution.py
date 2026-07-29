from app.manager import TaskManager
from app.tasks import AgentTask
from app.agents.context import AgentContext


class ExecutionService:
    """
    Entry point for OneMind execution pipeline.
    """

    def __init__(
        self,
        task_manager: TaskManager,
        agent_invoker,
    ):
        self.task_manager = task_manager
        self.agent_invoker = agent_invoker


    async def execute(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Execute AgentTask through execution pipeline.
        """

        context = AgentContext(
            request_id=task.task_id,
            metadata={
                "task_id": task.task_id,
                "agent_id": task.agent_id,
            },
        )

        self.task_manager.create_task(
            task
        )

        self.task_manager.submit_task(
            task
        )

        result = await self.task_manager.execute_task(
            task,
            self.agent_invoker,
            context,
        )

        return result