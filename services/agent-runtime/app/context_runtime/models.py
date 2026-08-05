from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class ContextLifecycle(str, Enum):
    """
    Context lifecycle state.
    """

    CREATED = "created"
    ACTIVE = "active"
    STALE = "stale"
    ARCHIVED = "archived"
    REMOVED = "removed"


class ContextAllocation(BaseModel):
    """
    Token allocation breakdown.
    """

    system: int = 0
    memory: int = 0
    knowledge: int = 0
    conversation: int = 0
    reserved: int = 0


class ContextBudget(BaseModel):
    """
    Runtime token budget.

    Used by:
    - Context Runtime
    - Context Selector
    - Context Retrieval
    """

    max_tokens: int = Field(
        ...,
        gt=0,
    )

    allocation: ContextAllocation = Field(
        default_factory=ContextAllocation
    )

    consumed_tokens: int = 0

    reserved_tokens: int = 0

    @property
    def used_tokens(self) -> int:
        """
        Backward compatible alias.
        """

        return self.consumed_tokens

    @used_tokens.setter
    def used_tokens(
        self,
        value: int,
    ) -> None:
        """
        Backward compatible setter.
        """

        self.consumed_tokens = value

    @property
    def remaining_tokens(self) -> int:
        """
        Backward compatible remaining token alias.
        """

        return (
            self.max_tokens
            - self.consumed_tokens
            - self.reserved_tokens
        )

    def remaining(self) -> int:
        """
        Return remaining token budget.
        """

        return self.remaining_tokens

class ContextRefreshPolicy(BaseModel):
    """
    Policy controlling context refresh behavior.

    Used by:
    - Context Runtime
    - Context Lifecycle management
    """

    enabled: bool = True

    max_age_seconds: int = Field(
        default=3600,
        gt=0,
    )

    refresh_interval_seconds: int = Field(
        default=300,
        gt=0,
    )

    refresh_on_access: bool = True

    stale_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    relevance_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
    )

class ContextRuntimeState(BaseModel):
    """
    Runtime state for active context.

    Represents the context lifecycle object
    managed by ContextRuntimeCoordinator.
    """

    context_id: str

    lifecycle: ContextLifecycle = (
        ContextLifecycle.ACTIVE
    )

    budget: ContextBudget

    importance_score: float = 1.0

    last_refresh: datetime | None = None

    created_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )

    metadata: dict[str, object] = Field(
        default_factory=dict
    )


class ContextCandidate(BaseModel):
    """
    Candidate context unit.

    Used by:
    - Context Retriever
    - Context Ranker
    - Context Selector
    """

    context_id: str

    content: str | None = None

    score: float = 0.0

    lifecycle: ContextLifecycle = (
        ContextLifecycle.ACTIVE
    )

    budget: ContextBudget | None = None

    metadata: dict[str, object] = Field(
        default_factory=dict
    )


class SelectedContext(BaseModel):
    """
    Final selected context package.

    Consumed by:
    - Context Assembler
    - Agent Runtime
    """

    items: list[ContextCandidate] = Field(
        default_factory=list
    )

    total_tokens: int = 0

    total_score: float = 0.0

    metadata: dict[str, object] = Field(
        default_factory=dict
    )

    context_id: str | None = None

    content: str | None = None
