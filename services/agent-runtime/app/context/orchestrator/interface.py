"""
Context Orchestrator interface.

Defines the contract between Context Orchestration
service and concrete orchestration implementations.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from abc import ABC, abstractmethod

from .models import OrchestrationRequest, OrchestrationResult


class ContextOrchestrator(ABC):
    """
    Abstract contract for context orchestration.

    Implementations are responsible for coordinating
    context construction workflows.

    Future orchestration capabilities:

    - multi-source retrieval
    - context ranking
    - context prioritization
    - context compression
    - token budget management
    """

    @abstractmethod
    async def orchestrate(
        self,
        request: OrchestrationRequest,
    ) -> OrchestrationResult:
        """
        Execute context orchestration flow.

        Args:
            request:
                Context orchestration request.

        Returns:
            OrchestrationResult containing assembled context.
        """

        raise NotImplementedError
