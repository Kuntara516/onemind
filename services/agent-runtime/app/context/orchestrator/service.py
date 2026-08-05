"""
Context Orchestration Service.

Coordinates retrieval, ranking, and context assembly
within the Context Intelligence Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from app.context.orchestrator.models import (
    OrchestrationRequest,
    OrchestrationResult,
)


class ContextOrchestrationService:
    """
    Application service for Context Orchestration.

    Supports:

    1. Delegation mode

        ContextOrchestrationService(
            orchestrator
        )


    2. Pipeline mode

        ContextOrchestrationService(
            retrieval_service=...,
            ranking_service=...,
        )


    Responsibilities:

    - validate orchestration requests
    - coordinate retrieval pipeline
    - delegate ranking
    - assemble final context result
    - hide pipeline implementation details
    """

    def __init__(
        self,
        orchestrator=None,
        retrieval_service=None,
        ranking_service=None,
    ) -> None:
        """
        Initialize Context Orchestration Service.

        Args:

            orchestrator:
                Optional orchestration strategy.

            retrieval_service:
                Context retrieval implementation.

            ranking_service:
                Context ranking implementation.
        """

        self._orchestrator = orchestrator

        self._retrieval_service = (
            retrieval_service
        )

        self._ranking_service = (
            ranking_service
        )

    async def orchestrate(
        self,
        request: OrchestrationRequest,
    ) -> OrchestrationResult:
        """
        Execute context orchestration.

        Supports:

        Strategy delegation:

            Request
                |
                v
            Orchestrator
                |
                v
            Result


        Pipeline execution:

            Request
                |
                v
            Retrieval Service
                |
                v
            Ranking Service
                |
                v
            Result
        """

        if request is None:
            raise ValueError(
                "Orchestration request cannot be None"
            )

        #
        # Strategy delegation mode
        #
        if self._orchestrator is not None:
            return await self._orchestrator.orchestrate(
                request
            )

        #
        # Retrieval + Ranking pipeline mode
        #
        if (
            self._retrieval_service is None
            or self._ranking_service is None
        ):
            raise RuntimeError(
                "Context orchestration services are not configured"
            )

        retrieval_result = (
            await self._retrieval_service.retrieve(
                request.context,
            )
        )

        ranking_result = (
            await self._ranking_service.rank(
                retrieval_result,
            )
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
