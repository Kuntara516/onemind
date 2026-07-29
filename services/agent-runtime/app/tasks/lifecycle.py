from app.tasks.status import TaskStatus


class InvalidTaskTransition(Exception):
    """Raised when an invalid task state transition is requested."""

    pass


class TaskLifecycle:
    """
    Responsible for validating AgentTask lifecycle transitions.

    Lifecycle:

    CREATED
        |
        v
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

    _allowed_transitions = {
        TaskStatus.CREATED: {
            TaskStatus.QUEUED,
        },
        TaskStatus.QUEUED: {
            TaskStatus.RUNNING,
        },
        TaskStatus.RUNNING: {
            TaskStatus.COMPLETED,
            TaskStatus.FAILED,
        },
        TaskStatus.COMPLETED: set(),
        TaskStatus.FAILED: set(),
    }

    @classmethod
    def can_transition(
        cls,
        current_status: TaskStatus,
        next_status: TaskStatus,
    ) -> bool:
        """
        Check whether a lifecycle transition is allowed.
        """

        return next_status in cls._allowed_transitions.get(
            current_status,
            set(),
        )

    @classmethod
    def transition(
        cls,
        current_status: TaskStatus,
        next_status: TaskStatus,
    ) -> TaskStatus:
        """
        Validate and perform lifecycle transition.

        Returns:
            New TaskStatus

        Raises:
            InvalidTaskTransition
            if transition is not allowed.
        """

        if not cls.can_transition(
            current_status,
            next_status,
        ):
            raise InvalidTaskTransition(
                f"Invalid task transition: "
                f"{current_status} -> {next_status}"
            )

        return next_status