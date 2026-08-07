"""
Context Runtime Integration

Sprint:
    S4-008 Context Runtime Integration
    S4-009 Context Runtime Observability

Bridges Context Intelligence pipeline
with Agent Runtime execution context.

Adds runtime tracing and observability
without changing existing pipeline contracts.
"""

from __future__ import annotations

from app.tasks import AgentTask
from app.agents.context import AgentContext

from .retriever import ContextRetriever
from .ranker import ContextRanker
from .selector import ContextSelector
from .assembler import ContextAssembler

from .policies import SelectionPolicy
from .assembly_models import AssembledContext

from .observability import (
    ContextObservabilityService,
    ContextRuntimeEvent,
)


class ContextRuntimeIntegration:
    """
    Integration layer between:

    Agent Runtime
        |
        v
    Context Intelligence Pipeline

    Pipeline:

        Retrieve
            |
        Rank
            |
        Select
            |
        Assemble

    Observability:

        Trace
          |
          +-- Retrieval events
          +-- Ranking events
          +-- Selection events
          +-- Assembly events
    """

    def __init__(
        self,
        retriever: ContextRetriever,
        ranker: ContextRanker,
        selector: ContextSelector,
        assembler: ContextAssembler,
        selection_policy: SelectionPolicy | None = None,
        observability: ContextObservabilityService | None = None,
    ):
        self.retriever = retriever
        self.ranker = ranker
        self.selector = selector
        self.assembler = assembler

        self.selection_policy = (
            selection_policy
            or SelectionPolicy()
        )

        self.observability = (
            observability
            or ContextObservabilityService()
        )

    def build_context(
        self,
        task: AgentTask,
        agent_context: AgentContext,
    ) -> AssembledContext:
        """
        Build runtime context package
        from AgentTask.

        Returns:
            AssembledContext
        """

        trace = self.observability.start_trace(
            task_id=str(
                getattr(task, "id", None)
            ),
        )

        try:
            query = self._build_query(
                task
            )

            #
            # Retrieval
            #
            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.RETRIEVAL_STARTED,
            )

            candidates = self.retriever.retrieve(
                query=query,
            )

            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.RETRIEVAL_COMPLETED,
                metadata={
                    "retrieved_items": len(
                        candidates
                    ),
                },
            )

            #
            # Ranking
            #
            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.RANKING_STARTED,
            )

            ranked = self.ranker.rank(
                candidates=candidates,
                query=query,
            )

            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.RANKING_COMPLETED,
                metadata={
                    "ranked_items": len(
                        ranked
                    ),
                },
            )

            #
            # Selection
            #
            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.SELECTION_STARTED,
            )

            selected = self.selector.select(
                candidates=ranked,
                policy=self.selection_policy,
            )

            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.SELECTION_COMPLETED,
                metadata={
                    "selected_items": len(
                        selected.items
                    ),
                },
            )

            #
            # Assembly
            #
            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.ASSEMBLY_STARTED,
            )

            assembled = self.assembler.assemble(
                selected_context=selected,
                user_input=query,
            )

            self.observability.record_event(
                trace.trace_id,
                ContextRuntimeEvent.ASSEMBLY_COMPLETED,
                metadata={
                    "sections": assembled.section_count,
                },
            )

            #
            # Metrics
            #
            self.observability.update_metrics(
                trace.trace_id,
                retrieved_items=len(
                    candidates
                ),
                ranked_items=len(
                    ranked
                ),
                selected_items=len(
                    selected.items
                ),
                compressed_tokens=(
                    getattr(
                        assembled,
                        "total_tokens",
                        0,
                    )
                ),
            )

            summary = self.observability.finish_trace(
                trace.trace_id,
            )

            #
            # Preserve existing context contract
            #
            agent_context.set(
                "assembled_context",
                assembled,
            )

            agent_context.set(
                "context_runtime",
                {
                    "enabled": True,
                    "pipeline": [
                        "retrieval",
                        "ranking",
                        "selection",
                        "assembly",
                    ],
                    "selected_items": len(
                        selected.items
                    ),
                },
            )

            agent_context.set(
                "context_runtime_observability",
                summary.model_dump(),
            )

            return assembled

        except Exception:
            self.observability.finish_trace(
                trace.trace_id,
                success=False,
            )

            raise

    @staticmethod
    def _build_query(
        task: AgentTask,
    ) -> str:
        """
        Create retrieval query from task.
        """

        parts = [
            task.intent,
        ]

        if task.input:
            parts.append(
                str(task.input)
            )

        return " ".join(parts)
