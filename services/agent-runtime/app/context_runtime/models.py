from __future__ import annotations

from datetime import datetime, UTC
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class ContextLifecycle(str, Enum):
    """Lifecycle state of a runtime context."""

    ACTIVE = "active"
    STALE = "stale"
    ARCHIVED = "archived"
    REMOVED = "removed"


class ContextAllocation(BaseModel):
    """Token allocation across context sources."""

    system: int = Field(default=0, ge=0)
    memory: int = Field(default=0, ge=0)
    knowledge: int = Field(default=0, ge=0)
    conversation: int = Field(default=0, ge=0)
    reserved: int = Field(default=0, ge=0)


class ContextBudget(BaseModel):
    """Token budget configuration."""

    max_tokens: int = Field(..., gt=0)
    used_tokens: int = Field(default=0, ge=0)

    allocation: ContextAllocation = Field(
        default_factory=ContextAllocation
    )


class ContextRefreshPolicy(BaseModel):
    """Policy controlling runtime refresh."""

    enabled: bool = True

    relevance_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
    )

    refresh_interval_seconds: int = Field(
        default=300,
        ge=1,
    )


class ContextRuntimeState(BaseModel):
    """Runtime state of an active context."""

    context_id: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    last_refresh: Optional[datetime] = None

    lifecycle: ContextLifecycle = ContextLifecycle.ACTIVE

    importance_score: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )

    metadata: Dict[str, str] = Field(
        default_factory=dict
    )

    budget: ContextBudget

    refresh_policy: ContextRefreshPolicy = Field(
        default_factory=ContextRefreshPolicy
    )
