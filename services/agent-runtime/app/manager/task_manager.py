from app.tasks import AgentTask, TaskStatus
from app.tasks.lifecycle import TaskLifecycle


class TaskManager:
    """
    Coordinates AgentTask execution lifecycle.

    Responsibilities:
    - create task
    - submit task
    - execute task through Executor
    - track task status

    TaskManager does not:
    - execute capabilities directly
    - contain business logic
    """

    def __init__(self, executor):
        """
        Initialize TaskManager.

        Args:
            executor:
                Executor instance responsible for task execution.
        """

        self.executor = executor
        self.tasks: dict[str, AgentTask] = {}

    def create_task(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Register a new AgentTask.

        Initial lifecycle state:

        CREATED
        """

        self.tasks[task.task_id] = task

        return task

    def submit_task(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Submit task into execution pipeline.

        Lifecycle transition:

        CREATED -> QUEUED
        """

        task.status = TaskLifecycle.transition(
            task.status,
            TaskStatus.QUEUED,
        )

        self.tasks[task.task_id] = task

        return task

    async def execute_task(
        self,
        task: AgentTask,
        capability_manager,
    ) -> AgentTask:
        """
        Execute task through Executor.

        Executor owns:
        - capability resolution
        - capability execution

        TaskManager owns:
        - coordination
        - tracking
        """

        result = await self.executor.execute(
            task,
            capability_manager,
        )

        self.tasks[task.task_id] = result

        return result

    def get_task_status(
        self,
        task_id: str,
    ) -> TaskStatus:
        """
        Return current task lifecycle state.
        """

        task = self.tasks.get(task_id)

        if task is None:
            raise KeyError(
                f"Task not found: {task_id}"
            )

        return task.status