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
    - execute agents directly
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
        agent_invoker,
        context,
        trace,
    ) -> AgentTask:
        """
        Execute task through Executor.

        Executor owns:
        - execution coordination
        - agent invocation

        AgentInvoker owns:
        - agent resolution
        - agent execution
        - capability injection

        TaskManager owns:
        - coordination
        - tracking
        """

        result = await self.executor.execute(
            task,
            agent_invoker,
            context,
            trace,
        )

        self.tasks[task.task_id] = result

        return result

    def get_task_status(
        self,
        task_id: str,
    ) -> TaskStatus:
        """
        Return current lifecycle state.
        """

        task = self.tasks.get(task_id)

        if task is None:
            raise KeyError(
                f"Task not found: {task_id}"
            )

        return task.status