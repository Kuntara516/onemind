"""
Context builder interfaces.

Defines contracts for context construction strategies.
"""

from abc import ABC, abstractmethod

from .models import ContextRequest, ContextResult


class ContextBuilder(ABC):
    """
    Abstract interface for building agent context.
    """

    @abstractmethod
    async def build(
        self,
        request: ContextRequest,
    ) -> ContextResult:
        """
        Build context from a context request.

        Implementations may retrieve:
        - memories
        - knowledge
        - runtime state
        """

        raise NotImplementedError
