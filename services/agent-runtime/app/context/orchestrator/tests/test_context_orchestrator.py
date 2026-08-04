"""
OneMind Context Orchestration Tests.

Validates Context Orchestrator implementation.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

import pytest

from app.context.models import ContextRequest, ContextResult
from app.context.orchestrator.models import (
    OrchestrationRequest,
)
from app.context.orchestrator.service import (
    ContextOrchestrationService,
)
from app.context.orchestrator.strategies.default import (
    DefaultContextOrchestrator,
)


class MockContextService:
    """
    Mock Context Service for orchestration tests.
    """

    async def build_context(
        self,
        request: ContextRequest,
    ) -> ContextResult:
        """
        Return deterministic context result.
        """

        return ContextResult(
            memories=[
                {
                    "content": request.user_input,
                }
            ],
            metadata={
                "source": "mock",
            },
        )


@pytest.mark.anyio
async def test_default_context_orchestrator_builds_context():
    """
    Validate DefaultContextOrchestrator delegates
    context building correctly.
    """

    context_service = MockContextService()

    orchestrator = DefaultContextOrchestrator(
        context_service,
    )

    result = await orchestrator.orchestrate(
        OrchestrationRequest(
            context=ContextRequest(
                user_input="OneMind orchestration",
            )
        )
    )

    assert len(result.context.memories) == 1

    assert (
        result.context.memories[0]["content"]
        == "OneMind orchestration"
    )

    assert result.metadata["strategy"] == "default"

    assert (
        "context_orchestration_completed"
        in result.trace
    )


@pytest.mark.anyio
async def test_context_orchestration_service_delegates():
    """
    Validate ContextOrchestrationService delegates
    execution to orchestrator.
    """

    context_service = MockContextService()

    orchestrator = DefaultContextOrchestrator(
        context_service,
    )

    service = ContextOrchestrationService(
        orchestrator,
    )

    result = await service.orchestrate(
        OrchestrationRequest(
            context=ContextRequest(
                user_input="service delegation",
            )
        )
    )

    assert isinstance(
        result.context,
        ContextResult,
    )

    assert (
        result.metadata["strategy"]
        == "default"
    )


@pytest.mark.anyio
async def test_context_orchestration_empty_request():
    """
    Validate empty orchestration request validation.
    """

    context_service = MockContextService()

    orchestrator = DefaultContextOrchestrator(
        context_service,
    )

    service = ContextOrchestrationService(
        orchestrator,
    )

    with pytest.raises(ValueError):
        await service.orchestrate(
            None,
        )
