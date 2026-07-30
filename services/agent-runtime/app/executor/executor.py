from datetime import datetime, timezone

from app.tasks import (
    AgentTask,
    TaskStatus,
    TaskLifecycle,
)

from app.runtime.invocation_request import (
    AgentInvocationRequest,
)

from app.runtime.tracing import (
    ExecutionTrace,
    EventType,
)

class Executor:
    """
    Executes AgentTask through Agent Runtime.

    Executor responsibilities:
    - lifecycle coordination
    - agent invocation
    - result handling
    - execution metadata update
    - execution trace event recording
    """

    async def execute(
        self,
        task: AgentTask,
        agent_invoker,
        context,
        trace: ExecutionTrace,
    ) -> AgentTask:
        """
        Execute AgentTask.

        Lifecycle:

        QUEUED
            |
            v
        RUNNING
            |
            +------------+
            |            |
            v            v
        COMPLETED      FAILED
        """

        try:
            task.status = TaskLifecycle.transition(
                task.status,
                TaskStatus.RUNNING,
            )

            trace.add_event(
                EventType.AGENT_STARTED,
                agent=task.agent_id,
            )

            invocation_request = AgentInvocationRequest(
                agent_id=task.agent_id,
                task=task,
                context=context,
            )

            invocation_result = await agent_invoker.invoke(
                invocation_request
            )

            if not invocation_result.success:
                raise Exception(
                    invocation_result.error
                )

            task.result = invocation_result.output

            trace.add_event(
                EventType.AGENT_FINISHED,
                agent=task.agent_id,
            )

            task.status = TaskLifecycle.transition(
                task.status,
                TaskStatus.COMPLETED,
            )

            task.completed_at = datetime.now(
                timezone.utc
            )

            return task

        except Exception as exc:
            task.result = {
                "error": "execution_failed",
                "message": str(exc),
            }

            trace.add_event(
                EventType.ERROR,
                message=str(exc),
            )

            task.status = TaskLifecycle.transition(
                task.status,
                TaskStatus.FAILED,
            )

            return task