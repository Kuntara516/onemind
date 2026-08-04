from __future__ import annotations

from app.context_runtime.interface import ContextBudgetManager
from app.context_runtime.models import ContextBudget


class DefaultContextBudgetManager(ContextBudgetManager):
    """
    Default implementation for context token budget management.
    """

    def __init__(self) -> None:
        self._budget: ContextBudget | None = None

    def allocate(
        self,
        budget: ContextBudget,
    ) -> ContextBudget:
        """
        Set active context budget.
        """

        self._budget = budget

        return self._budget

    def consume(
        self,
        tokens: int,
    ) -> ContextBudget:
        """
        Consume tokens from current budget.
        """

        if self._budget is None:
            raise RuntimeError(
                "Context budget has not been allocated"
            )

        if tokens < 0:
            raise ValueError(
                "Consumed tokens must be non-negative"
            )

        if self.remaining() < tokens:
            raise ValueError(
                "Insufficient context budget"
            )

        self._budget.used_tokens += tokens

        return self._budget

    def remaining(
        self,
    ) -> int:
        """
        Return remaining available tokens.
        """

        if self._budget is None:
            return 0

        return (
            self._budget.max_tokens
            - self._budget.used_tokens
        )
