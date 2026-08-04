"""
Context Orchestration models.

Defines request and response contracts for the
Context Orchestration Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from typing import Any

from pydantic import BaseModel, Field

from app.context.models import ContextRequest, ContextResult


class OrchestrationRequest(BaseModel):
    """
    Input request for Context Orchestration.

    Wraps the ContextRequest and provides orchestration
    metadata for future pipeline extensions.
    """

    context: ContextRequest

    metadata: dict[str, Any] = Field(default_factory=dict)


class OrchestrationResult(BaseModel):
    """
    Result produced by Context Orchestrator.

    Wraps the ContextResult and exposes orchestration
    metadata for future enhancements such as:

    - retrieval ranking
    - source prioritization
    - token budgeting
    - execution tracing
    """

    context: ContextResult

    metadata: dict[str, Any] = Field(default_factory=dict)

    trace: list[str] = Field(default_factory=list)
