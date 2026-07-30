from app.manager import TaskManager
from app.tasks import AgentTask
from app.agents.context import AgentContext
from app.runtime.tracing import (
    ExecutionTrace,
    TraceRecorder,
    EventType,
)

class ExecutionService:
    """
    Entry point for OneMind execution pipeline.
    """

    def __init__(
        self,
        task_manager: TaskManager,
        agent_invoker,
        trace_recorder: TraceRecorder,
    ):
        self.task_manager = task_manager
        self.agent_invoker = agent_invoker
        self.trace_recorder = trace_recorder


    async def execute(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Execute AgentTask through execution pipeline.
        """
        trace = ExecutionTrace(
            request_id=task.task_id,
            task_id=task.task_id,
        )

        trace.add_event(
            EventType.EXECUTION_STARTED
        )

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
            trace,
        )

        trace.add_event(
            EventType.EXECUTION_FINISHED
        )

        trace.finish()

        self.trace_recorder.record(
            trace
        )

        return result