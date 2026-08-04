from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class ContextLifecycle:
    """
    Context runtime lifecycle states.

    State transition:

        CREATED
            |
            v
        ACTIVE
            |
            v
        STALE
            |
            v
        ARCHIVED
            |
            v
        REMOVED
    """

    CREATED = "created"

    ACTIVE = "active"

    STALE = "stale"

    ARCHIVED = "archived"

    REMOVED = "removed"


class ContextAllocation(BaseModel):
    """
    Token allocation across context sources.
    """

    system: int = Field(
        default=0,
        ge=0,
    )

    memory: int = Field(
        default=0,
        ge=0,
    )

    knowledge: int = Field(
        default=0,
        ge=0,
    )

    conversation: int = Field(
        default=0,
        ge=0,
    )

    reserved: int = Field(
        default=0,
        ge=0,
    )


class ContextBudget(BaseModel):
    """
    Runtime context token budget.
    """

    max_tokens: int = Field(
        ...,
        gt=0,
    )

    used_tokens: int = Field(
        default=0,
        ge=0,
    )

    allocation: ContextAllocation

    def remaining_tokens(self) -> int:
        """
        Return remaining available tokens.
        """

        return (
            self.max_tokens
            - self.used_tokens
        )


class ContextRefreshPolicy(BaseModel):
    """
    Context refresh configuration.
    """

    enabled: bool = Field(
        default=True,
    )

    relevance_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
    )

    refresh_interval_seconds: int = Field(
        default=300,
        gt=0,
    )


class ContextRuntimeState(BaseModel):
    """
    Runtime state of an active context.

    Represents the lifecycle-managed
    execution context container.
    """

    context_id: str

    lifecycle: str = Field(
        default=ContextLifecycle.CREATED,
    )

    created_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc),
    )

    updated_at: datetime = Field(
        default_factory=lambda:
            datetime.now(timezone.utc),
    )

    budget: ContextBudget

    refresh_policy: ContextRefreshPolicy = Field(
        default_factory=ContextRefreshPolicy,
    )

    metadata: Optional[dict] = Field(
        default=None,
    )

    def touch(self) -> None:
        """
        Update last modified timestamp.
        """

        self.updated_at = datetime.now(
            timezone.utc
        )
