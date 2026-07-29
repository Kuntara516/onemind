from datetime import datetime, timezone

from app.tasks import (
    AgentTask,
    TaskStatus,
    TaskLifecycle,
)

from app.runtime.invocation_request import (
    AgentInvocationRequest,
)


class Executor:
    """
    Executes AgentTask through Agent Runtime.

    Executor responsibilities:
    - lifecycle coordination
    - agent invocation
    - result handling
    - execution metadata update
    """

    async def execute(
        self,
        task: AgentTask,
        agent_invoker,
        context,
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

            task.status = TaskLifecycle.transition(
                task.status,
                TaskStatus.FAILED,
            )

            return task