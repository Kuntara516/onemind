"""
Context Orchestration Service.

Coordinates retrieval, ranking, and context assembly
within the Context Intelligence Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from app.context.orchestrator.interface import (
    ContextOrchestratorInterface,
)

from app.context.orchestrator.models import (
    OrchestrationRequest,
    OrchestrationResult,
)


class ContextOrchestrationService:
    """
    Application service for Context Orchestration.

    Responsibilities:
    - validate orchestration requests
    - coordinate retrieval pipeline
    - delegate ranking
    - assemble final context result
    - hide pipeline implementation details
    """

    def __init__(
        self,
        retrieval_service,
        ranking_service,
    ) -> None:
        """
        Initialize Context Orchestration Service.

        Args:
            retrieval_service:
                Retrieval service implementation.

            ranking_service:
                Context ranking service implementation.
        """

        self._retrieval_service = retrieval_service
        self._ranking_service = ranking_service

    async def orchestrate(
        self,
        request: OrchestrationRequest,
    ) -> OrchestrationResult:
        """
        Execute context orchestration pipeline.

        Pipeline:

        ContextRequest
            |
            v
        Retrieval Service
            |
            v
        Ranking Service
            |
            v
        OrchestrationResult

        Args:
            request:
                Context orchestration request.

        Returns:
            Orchestration result.
        """

        if request is None:
            raise ValueError(
                "Orchestration request cannot be None"
            )

        retrieval_result = await self._retrieval_service.retrieve(
            request.context,
        )

        ranking_result = await self._ranking_service.rank(
            retrieval_result,
        )

        return OrchestrationResult(
            context=ranking_result,
            metadata=request.metadata,
            trace=[
                "retrieval_completed",
                "ranking_completed",
                "context_assembled",
            ],
        )
