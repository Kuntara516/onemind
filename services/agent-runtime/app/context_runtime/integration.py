"""
Context Runtime Integration

Sprint:
    S4-008 Context Runtime Integration
    S4-009 Context Runtime Observability

Bridges Context Intelligence pipeline
with Agent Runtime execution context.

Adds:
    - Runtime tracing
    - Stage timing
    - Pipeline metrics
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
            |
        Observability
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

        Includes observability tracing.
        """

        trace = self.observability.start_trace(
            task_id=str(
                getattr(
                    task,
                    "id",
                    "",
                )
            ),
        )

        trace_id = trace.trace_id

        try:
            query = self._build_query(
                task
            )

            #
            # Retrieval Stage
            #
            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.RETRIEVAL_STARTED,
            )

            self.observability.start_stage(
                trace_id,
                "retrieval",
            )

            candidates = self.retriever.retrieve(
                query=query,
            )

            self.observability.complete_stage(
                trace_id,
                "retrieval",
            )

            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.RETRIEVAL_COMPLETED,
                metadata={
                    "items": len(candidates),
                },
            )

            #
            # Ranking Stage
            #
            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.RANKING_STARTED,
            )

            self.observability.start_stage(
                trace_id,
                "ranking",
            )

            ranked = self.ranker.rank(
                candidates=candidates,
                query=query,
            )

            self.observability.complete_stage(
                trace_id,
                "ranking",
            )

            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.RANKING_COMPLETED,
                metadata={
                    "items": len(ranked),
                },
            )

            #
            # Selection Stage
            #
            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.SELECTION_STARTED,
            )

            self.observability.start_stage(
                trace_id,
                "selection",
            )

            selected = self.selector.select(
                candidates=ranked,
                policy=self.selection_policy,
            )

            self.observability.complete_stage(
                trace_id,
                "selection",
            )

            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.SELECTION_COMPLETED,
                metadata={
                    "items": len(
                        selected.items
                    ),
                },
            )

            #
            # Assembly Stage
            #
            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.ASSEMBLY_STARTED,
            )

            self.observability.start_stage(
                trace_id,
                "assembly",
            )

            assembled = self.assembler.assemble(
                selected_context=selected,
                user_input=query,
            )

            self.observability.complete_stage(
                trace_id,
                "assembly",
            )

            self.observability.record_event(
                trace_id,
                ContextRuntimeEvent.ASSEMBLY_COMPLETED,
            )

            #
            # Metrics
            #
            self.observability.update_metrics(
                trace_id,
                retrieved_items=len(
                    candidates
                ),
                ranked_items=len(
                    ranked
                ),
                selected_items=len(
                    selected.items
                ),
                original_tokens=(
                    assembled.total_tokens
                    if hasattr(
                        assembled,
                        "total_tokens",
                    )
                    else 0
                ),
            )

            summary = self.observability.finish_trace(
                trace_id,
                success=True,
            )

            #
            # Agent Runtime Context
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
                    "trace_id": str(
                        trace_id
                    ),
                },
            )

            agent_context.set(
                "context_runtime_observability",
                summary,
            )

            return assembled

        except Exception:

            self.observability.finish_trace(
                trace_id,
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
                str(
                    task.input
                )
            )

        return " ".join(parts)
