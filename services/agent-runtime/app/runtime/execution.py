from app.manager import TaskManager
from app.tasks import AgentTask


class ExecutionService:
    """
    Entry point for OneMind execution pipeline.
    """

    def __init__(
        self,
        task_manager: TaskManager,
        capability_manager,
    ):
        self.task_manager = task_manager
        self.capability_manager = capability_manager

    async def execute(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Execute AgentTask through execution pipeline.
        """

        self.task_manager.create_task(
            task
        )

        self.task_manager.submit_task(
            task
        )

        result = await self.task_manager.execute_task(
            task,
            self.capability_manager,
        )

        return result
