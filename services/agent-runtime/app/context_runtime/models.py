"""
Context Runtime Models

Defines runtime context state models used by:
- context lifecycle management
- context budget management
- context retrieval pipeline

S4-007-001 Context Runtime Foundation
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ContextLifecycle(str, Enum):
    """
    Context lifecycle states.
    """

    CREATED = "created"
    ACTIVE = "active"
    STALE = "stale"
    ARCHIVED = "archived"
    REMOVED = "removed"


class ContextAllocation(BaseModel):
    """
    Token allocation breakdown for context budget.

    Represents reserved token capacity for each context source.
    """

    system: int = 0
    memory: int = 0
    knowledge: int = 0
    conversation: int = 0

    @property
    def total(self) -> int:
        """
        Calculate total allocated tokens.
        """

        return (
            self.system
            + self.memory
            + self.knowledge
            + self.conversation
        )


class ContextBudget(BaseModel):
    """
    Context token budget model.
    """

    max_tokens: int

    allocation: ContextAllocation

    consumed_tokens: int = 0
    reserved_tokens: int = 0

    @property
    def used_tokens(self) -> int:
        """
        Backward compatibility alias.

        Existing BudgetManager expects:

            budget.used_tokens

        Context Runtime model uses:

            budget.consumed_tokens

        consumed_tokens remains the source of truth.
        """

        return self.consumed_tokens

    @used_tokens.setter
    def used_tokens(self, value: int) -> None:
        """
        Backward compatibility setter.

        Supports existing mutation logic:

            budget.used_tokens += tokens

        while maintaining:

            consumed_tokens

        as the canonical value.
        """

        self.consumed_tokens = value

    @property
    def remaining_tokens(self) -> int:
        """
        Calculate remaining available tokens.
        """

        return (
            self.max_tokens
            - self.consumed_tokens
            - self.reserved_tokens
        )


class ContextRuntimeState(BaseModel):
    """
    Runtime state container for a context session.
    """

    context_id: str

    lifecycle: ContextLifecycle = (
        ContextLifecycle.CREATED
    )

    budget: Optional[ContextBudget] = None

    metadata: dict = Field(
        default_factory=dict
    )

    created_at: Optional[str] = None

    updated_at: Optional[str] = None

    def is_active(self) -> bool:
        """
        Check whether context is active.
        """

        return (
            self.lifecycle
            == ContextLifecycle.ACTIVE
        )

    def is_removed(self) -> bool:
        """
        Check whether context is removed.
        """

        return (
            self.lifecycle
            == ContextLifecycle.REMOVED
        )
