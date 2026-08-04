from __future__ import annotations

from app.context_runtime.budget import (
    DefaultContextBudgetManager,
)
from app.context_runtime.lifecycle import (
    DefaultContextLifecycleManager,
)
from app.context_runtime.models import (
    ContextBudget,
    ContextRuntimeState,
)


class ContextRuntimeCoordinator:
    """
    Coordinates context runtime operations.

    Responsible for composing:
    - Budget management
    - Lifecycle management
    """

    def __init__(self) -> None:
        self._budget_manager = (
            DefaultContextBudgetManager()
        )

        self._lifecycle_manager = (
            DefaultContextLifecycleManager()
        )

        self._context: ContextRuntimeState | None = None

    def create_context(
        self,
        context_id: str,
        budget: ContextBudget,
    ) -> ContextRuntimeState:
        """
        Create runtime context.
        """

        self._context = ContextRuntimeState(
            context_id=context_id,
            budget=budget,
        )

        self._budget_manager.allocate(
            budget
        )

        return self._context

    def activate_context(
        self,
    ) -> ContextRuntimeState:
        """
        Activate current context.
        """

        self._require_context()

        return self._lifecycle_manager.activate(
            self._context
        )

    def consume_tokens(
        self,
        tokens: int,
    ) -> ContextRuntimeState:
        """
        Consume context tokens.
        """

        self._require_context()

        self._budget_manager.consume(
            tokens
        )

        return self._context

    def remaining_budget(
        self,
    ) -> int:
        """
        Return remaining context budget.
        """

        return self._budget_manager.remaining()

    def archive_context(
        self,
    ) -> ContextRuntimeState:
        """
        Archive current context.
        """

        self._require_context()

        return self._lifecycle_manager.archive(
            self._context
        )

    def remove_context(
        self,
    ) -> ContextRuntimeState:
        """
        Remove current context.
        """

        self._require_context()

        return self._lifecycle_manager.remove(
            self._context
        )

    def get_context(
        self,
    ) -> ContextRuntimeState | None:
        """
        Return current runtime context.
        """

        return self._context

    def _require_context(
        self,
    ) -> None:
        """
        Ensure context exists.
        """

        if self._context is None:
            raise RuntimeError(
                "Context has not been created"
            )
