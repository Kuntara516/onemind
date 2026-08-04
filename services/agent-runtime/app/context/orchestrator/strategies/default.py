"""
Default context orchestration strategy.

Provides the initial orchestration flow by coordinating
Context Builder and Retrieval Pipeline components.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from app.context.models import ContextRequest
from app.context.service import ContextService

from ..interface import ContextOrchestrator
from ..models import OrchestrationRequest, OrchestrationResult


class DefaultContextOrchestrator(ContextOrchestrator):
    """
    Default implementation of Context Orchestrator.

    Current responsibilities:

    - delegate context construction
    - coordinate existing context pipeline
    - assemble orchestration result

    Future extensions:

    - multi-source retrieval
    - context ranking
    - source prioritization
    - token budgeting
    - context compression
    """

    def __init__(
        self,
        context_service: ContextService,
    ) -> None:
        """
        Initialize default context orchestrator.

        Args:
            context_service:
                ContextService instance.
        """

        self._context_service = context_service

    async def orchestrate(
        self,
        request: OrchestrationRequest,
    ) -> OrchestrationResult:
        """
        Execute default orchestration flow.

        Flow:

        OrchestrationRequest
                |
                v
        ContextRequest
                |
                v
        ContextService
                |
                v
        ContextResult
                |
                v
        OrchestrationResult

        Args:
            request:
                Context orchestration request.

        Returns:
            Orchestration result.
        """

        context_result = await self._context_service.build_context(
            request.context,
        )

        return OrchestrationResult(
            context=context_result,
            metadata={
                "strategy": "default",
            },
            trace=[
                "context_orchestration_started",
                "context_builder_executed",
                "context_orchestration_completed",
            ],
        )
