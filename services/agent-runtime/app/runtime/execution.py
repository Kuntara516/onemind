from app.context_runtime.integration import ContextRuntimeIntegration
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

    ExecutionService is the integration boundary between
    Context Runtime and the existing Agent execution pipeline.

    Context Runtime enriches the AgentContext before the task
    enters TaskManager / Executor / AgentInvoker.
    """

    def __init__(
        self,
        task_manager: TaskManager,
        agent_invoker,
        trace_recorder: TraceRecorder,
        context_runtime: ContextRuntimeIntegration,
    ):
        self.task_manager = task_manager
        self.agent_invoker = agent_invoker
        self.trace_recorder = trace_recorder
        self.context_runtime = context_runtime

    async def execute(
        self,
        task: AgentTask,
    ) -> AgentTask:
        """
        Execute AgentTask through the execution pipeline.

        Context Runtime is invoked after AgentContext creation and
        before downstream task execution. The same AgentContext
        instance is passed through the existing execution pipeline.
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

        self.context_runtime.build_context(
            task,
            context,
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
