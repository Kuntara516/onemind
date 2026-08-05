"""
Context Orchestrator Interface.

Defines the contract between Context Orchestration
service and concrete orchestration implementations.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from abc import ABC, abstractmethod

from .models import (
    OrchestrationRequest,
    OrchestrationResult,
)


class ContextOrchestratorInterface(ABC):
    """
    Abstract contract for context orchestration.

    Implementations are responsible for coordinating
    context intelligence workflows.

    Future orchestration capabilities:

    - multi-source retrieval
    - context ranking
    - context prioritization
    - context compression
    - token budget management
    - execution tracing
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
            OrchestrationResult containing
            assembled context.
        """

        raise NotImplementedError


# ---------------------------------------------------------------------
# Backward compatible contract name.
#
# Existing orchestrator implementations and tests
# expect ContextOrchestrator.
#
# Keep ContextOrchestratorInterface as the canonical
# interface name while exposing the historical name.
# ---------------------------------------------------------------------

ContextOrchestrator = ContextOrchestratorInterface
