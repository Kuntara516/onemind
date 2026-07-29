from datetime import datetime, timezone

from app.tasks import (
    AgentTask,
    TaskStatus,
    TaskLifecycle,
)


class Executor:
    """
    Executes AgentTask through available capabilities.

    Executor responsibilities:
    - lifecycle coordination
    - capability invocation
    - result handling
    - execution metadata update
    """

    async def execute(
        self,
        task: AgentTask,
        capability_manager,
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

            capability = capability_manager.resolve(
                task.required_capabilities
            )

            result = await capability.execute(
                **task.input
            )

            task.result = result

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