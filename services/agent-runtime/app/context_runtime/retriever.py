"""
Context Retrieval Implementation

Provides context lookup capability
for S4 Context Intelligence pipeline.

S4-007-001
"""

from abc import ABC, abstractmethod

from .models import ContextCandidate


class ContextRetriever(ABC):
    """
    Abstract interface for context retrieval.

    Future implementations may connect:
    - Memory layer
    - Vector store
    - Knowledge retrieval
    - Hybrid RAG pipeline
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[ContextCandidate]:
        """
        Retrieve relevant context candidates.
        """
        raise NotImplementedError


class DefaultContextRetriever(ContextRetriever):
    """
    Default runtime context retriever.

    Current implementation:
        - retrieves from ContextRuntimeCoordinator
        - supports context id lookup
        - supports current active context retrieval

    Future:
        - semantic retrieval
        - vector similarity search
        - memory ranking
    """

    def __init__(
        self,
        coordinator=None,
    ):
        self._coordinator = coordinator


    def retrieve(
        self,
        query: str,
        limit: int = 5,
    ) -> list[ContextCandidate]:
        """
        Retrieve contexts by query.

        Current strategy:
            exact context id match.

        Future:
            embedding similarity search.
        """

        if self._coordinator is None:
            return []

        context = self.get_context(query)

        if context is None:
            return []

        return [context][:limit]


    def get_context(
        self,
        context_id: str,
    ) -> ContextCandidate | None:
        """
        Retrieve context candidate by id.
        """

        if self._coordinator is None:
            return None


        # ContextRuntimeCoordinator keeps
        # current context API.
        #
        # For multiple context lookup,
        # use internal runtime registry when available.

        contexts = getattr(
            self._coordinator,
            "_contexts",
            None,
        )

        if contexts is not None:
            context = contexts.get(context_id)

            if context is None:
                return None

            return ContextCandidate(
                context_id=context.context_id,
                lifecycle=context.lifecycle,
                budget=context.budget,
                score=1.0,
                source="runtime",
            )


        # fallback:
        # current context retrieval

        current = (
            self._coordinator.get_context()
        )

        if current is None:
            return None

        if current.context_id != context_id:
            return None


        return ContextCandidate(
            context_id=current.context_id,
            lifecycle=current.lifecycle,
            budget=current.budget,
            score=1.0,
            source="runtime",
        )


    def get_current(
        self,
    ) -> ContextCandidate | None:
        """
        Retrieve current runtime context.

        Returns:
            Current context candidate.
        """

        if self._coordinator is None:
            return None


        context = (
            self._coordinator.get_context()
        )

        if context is None:
            return None


        return ContextCandidate(
            context_id=context.context_id,
            lifecycle=context.lifecycle,
            budget=context.budget,
            score=1.0,
            source="runtime",
        )
