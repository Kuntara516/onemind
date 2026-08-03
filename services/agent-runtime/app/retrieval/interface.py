"""
Retrieval interface for Context Intelligence Layer.

Defines the contract between Retrieval Service
and concrete retrieval implementations.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from abc import ABC, abstractmethod

from .models import RetrievalRequest, RetrievalResult


class RetrievalInterface(ABC):
    """
    Abstract retrieval contract.

    Implementations may provide different retrieval
    strategies such as:

    - memory retrieval
    - knowledge retrieval
    - hybrid retrieval
    - external source retrieval
    """

    @abstractmethod
    async def retrieve(
        self,
        request: RetrievalRequest,
    ) -> RetrievalResult:
        """
        Retrieve relevant information.

        Args:
            request:
                Retrieval query and constraints.

        Returns:
            RetrievalResult containing retrieved data.
        """

        raise NotImplementedError
    
