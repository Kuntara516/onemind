from __future__ import annotations

from app.context_runtime.budget import (
    DefaultContextBudgetManager,
)

from app.context_runtime.control import (
    ContextRuntimeControlResult,
    ContextRuntimeDecisionController,
)

from app.context_runtime.evaluation.execution import (
    ContextRuntimeExecutionResult,
)

from app.context_runtime.lifecycle import (
    DefaultContextLifecycleManager,
)

from app.context_runtime.models import (
    ContextBudget,
    ContextLifecycle,
    ContextRuntimeState,
)

from app.context_runtime.refresh import (
    DefaultContextRefreshEngine,
)


class ContextRuntimeCoordinator:
    """
    Coordinates context runtime operations.

    Responsible for composing:
    - Budget management
    - Lifecycle management
    - Runtime decision execution
    """

    def __init__(
        self,
        decision_controller: ContextRuntimeDecisionController | None = None,
    ) -> None:
        self._budget_manager = (
            DefaultContextBudgetManager()
        )

        self._lifecycle_manager = (
            DefaultContextLifecycleManager()
        )

        self._decision_controller = (
            decision_controller
            or ContextRuntimeDecisionController(
                DefaultContextRefreshEngine()
            )
        )

        self._context: ContextRuntimeState | None = None

    def create_context(
        self,
        context_id: str,
        budget: ContextBudget,
    ) -> ContextRuntimeState:
        """
        Create runtime context.

        Newly created contexts always begin
        in CREATED lifecycle state.
        """

        self._context = ContextRuntimeState(
            context_id=context_id,
            budget=budget,
            lifecycle=ContextLifecycle.CREATED,
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

    def apply_decision(
        self,
        execution: ContextRuntimeExecutionResult,
    ) -> ContextRuntimeControlResult:
        """
        Apply an explicit runtime execution artifact.

        The coordinator remains the owner of runtime state;
        the decision controller owns action dispatch only.
        """

        self._require_context()

        result = self._decision_controller.apply(
            execution,
            self._context,
        )

        self._context = result.state

        return result

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
