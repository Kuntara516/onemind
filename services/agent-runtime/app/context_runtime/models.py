"""
Context runtime data models.

Defines runtime context state,
budget allocation, lifecycle state,
and retrieval candidate contracts.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ContextLifecycle(str, Enum):
    """
    Context lifecycle states.
    """

    CREATED = "created"

    ACTIVE = "active"

    STALE = " stale"

    ARCHIVED = "archived"

    REMOVED = "removed"


class ContextAllocation(BaseModel):
    """
    Token allocation distribution.

    Defines how context budget is divided
    across context sources.
    """

    system: int = 0

    memory: int = 0

    knowledge: int = 0

    conversation: int = 0


class ContextBudget(BaseModel):
    """
    Context token budget state.
    """

    max_tokens: int

    allocation: ContextAllocation

    consumed_tokens: int = 0

    reserved_tokens: int = 0

    @property
    def used_tokens(self) -> int:
        """
        Backward compatible alias.

        Budget manager uses used_tokens
        while storage keeps consumed_tokens.
        """

        return self.consumed_tokens

    @used_tokens.setter
    def used_tokens(self, value: int) -> None:
        """
        Allow budget manager mutation.
        """

        self.consumed_tokens = value

    @property
    def remaining_tokens(self) -> int:
        """
        Remaining available tokens.
        """

        return (
            self.max_tokens
            - self.consumed_tokens
            - self.reserved_tokens
        )


class ContextRuntimeState(BaseModel):
    """
    Runtime context state.

    Represents active context lifecycle
    and budget state.
    """

    context_id: str

    lifecycle: ContextLifecycle = (
        ContextLifecycle.CREATED
    )

    budget: ContextBudget

    metadata: dict[str, str] = Field(
        default_factory=dict
    )


class ContextCandidate(BaseModel):
    """
    Retrieved context candidate.

    Represents a context item returned
    from the context retrieval layer.

    This model becomes the contract between
    retrieval pipeline and context intelligence.
    """

    context_id: str

    score: float = 0.0

    lifecycle: ContextLifecycle

    budget: ContextBudget | None = None

    metadata: dict[str, str] = Field(
        default_factory=dict
    )
