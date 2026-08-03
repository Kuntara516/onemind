"""
Context models for Context Intelligence Layer.

This module defines request and response contracts
used by Context Builder implementations.
"""

from typing import Any

from pydantic import BaseModel, Field


class ContextRequest(BaseModel):
    """
    Input request for building context.

    This represents the information available before
    context retrieval and assembly.
    """

    task_id: str | None = None
    agent_id: str | None = None
    session_id: str | None = None

    user_input: str

    metadata: dict[str, Any] = Field(default_factory=dict)


class ContextResult(BaseModel):
    """
    Result produced by Context Builder.

    Designed to support future expansion:
    - memory retrieval
    - knowledge retrieval
    - runtime context
    - context compression
    """

    memories: list[Any] = Field(default_factory=list)

    knowledge: list[Any] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    token_budget: int | None = None
