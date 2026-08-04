"""
Context Orchestration service layer.

Provides application-level orchestration operations
for the OneMind Context Intelligence Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from .interface import ContextOrchestrator
from .models import OrchestrationRequest, OrchestrationResult


class ContextOrchestrationService:
    """
    Application service for context orchestration.

    This layer provides a stable API boundary between
    Agent Runtime components and orchestration strategies.

    Responsibilities:
    - validate orchestration requests
    - delegate orchestration execution
    - normalize orchestration results
    - hide implementation details
    """

    def __init__(
        self,
        orchestrator: ContextOrchestrator,
    ) -> None:
        """
        Initialize Context Orchestration Service.

        Args:
            orchestrator:
                Context orchestration implementation.
        """

        self._orchestrator = orchestrator

    async def orchestrate(
        self,
        request: OrchestrationRequest,
    ) -> OrchestrationResult:
        """
        Execute context orchestration.

        Args:
            request:
                Context orchestration request.

        Returns:
            Orchestration result.
        """

        if request is None:
            raise ValueError(
                "Orchestration request cannot be empty"
            )

        return await self._orchestrator.orchestrate(
            request,
        )
