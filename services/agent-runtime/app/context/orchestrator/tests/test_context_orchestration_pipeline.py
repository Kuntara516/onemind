"""
Context Orchestration Pipeline Tests.

Validates integration between:
- Retrieval Layer
- Ranking Layer
- Context Orchestration Layer

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

import pytest

from app.context.models import ContextRequest

from app.context.orchestrator.models import (
    OrchestrationRequest,
)

from app.context.orchestrator.service import (
    ContextOrchestrationService,
)


class MockRetrievalService:
    """
    Mock retrieval service.
    """

    async def retrieve(
        self,
        request,
    ):
        return [
            {
                "id": "memory-1",
                "content": "Relevant context",
            }
        ]


class MockRankingService:
    """
    Mock ranking service.
    """

    async def rank(
        self,
        request,
    ):
        return {
            "ranked": request,
        }


@pytest.mark.anyio
async def test_context_orchestration_pipeline():

    service = ContextOrchestrationService(
        retrieval_service=MockRetrievalService(),
        ranking_service=MockRankingService(),
    )

    result = await service.orchestrate(
        OrchestrationRequest(
            context=ContextRequest(
                user_input="test context",
            )
        )
    )

    assert result.context is not None

    assert result.trace == [
        "retrieval_completed",
        "ranking_completed",
        "context_assembled",
    ]


@pytest.mark.anyio
async def test_context_orchestration_empty_metadata():

    service = ContextOrchestrationService(
        retrieval_service=MockRetrievalService(),
        ranking_service=MockRankingService(),
    )

    result = await service.orchestrate(
        OrchestrationRequest(
            context=ContextRequest(
                user_input="empty metadata",
            )
        )
    )

    assert result.metadata == {}


@pytest.mark.anyio
async def test_context_orchestration_rejects_none_request():

    service = ContextOrchestrationService(
        retrieval_service=MockRetrievalService(),
        ranking_service=MockRankingService(),
    )

    with pytest.raises(ValueError):
        await service.orchestrate(None)
