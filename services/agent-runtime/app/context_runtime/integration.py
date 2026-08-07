```python
"""
Context Runtime Integration

Sprint:
    S4-008 Context Runtime Integration
    S4-009 Context Runtime Observability
    S4-010-004 Observability Runtime Integration

Bridges Context Intelligence pipeline
with Agent Runtime execution context.

Adds:

    - Runtime tracing
    - Stage timing
    - Pipeline metrics
    - Provider abstraction through
      ContextRuntimeObservabilityRuntime

Architecture:

    Agent Runtime
          |
          v
    ContextRuntimeIntegration
          |
          v
    ContextRuntimeObservabilityRuntime
          |
          v
    ObservabilityProviderManager
          |
    +-------------+-------------+
    |                           |
    v                           v
Memory Provider            OpenTelemetry

Author:
    OneMind Platform

License:
    MIT
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
    ContextRuntimeEvent,
)

from .observability.runtime import (
    ContextRuntimeObservabilityRuntime,
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
        Observability Runtime
    """

    def __init__(
        self,
        retriever: ContextRetriever,
        ranker: ContextRanker,
        selector: ContextSelector,
        assembler: ContextAssembler,
        selection_policy: SelectionPolicy | None = None,
        observability: ContextRuntimeObservabilityRuntime | None = None,
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
            or ContextRuntimeObservabilityRuntime()
        )

    def build_context(
        self,
        task: AgentTask,
        agent_context: AgentContext,
    ) -> AssembledContext:
        """
        Build runtime context package
        from AgentTask.

        Includes observability runtime tracing.
        """

        execution_id = str(
            getattr(
                task,
                "id",
                "",
            )
        )

        self.observability.start_trace(
            execution_id,
            attributes={
                "task_id": execution_id,
            },
        )

        try:

            query = self._build_query(
                task
            )

            #
            # Retrieval Stage
            #

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.RETRIEVAL_STARTED,
            )

            self.observability.start_stage(
                execution_id,
                "retrieval",
            )

            candidates = self.retriever.retrieve(
                query=query,
            )

            self.observability.finish_stage(
                execution_id,
                "retrieval",
                attributes={
                    "items": len(candidates),
                },
            )

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.RETRIEVAL_COMPLETED,
                attributes={
                    "items": len(candidates),
                },
            )


            #
            # Ranking Stage
            #

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.RANKING_STARTED,
            )

            self.observability.start_stage(
                execution_id,
                "ranking",
            )

            ranked = self.ranker.rank(
                candidates=candidates,
                query=query,
            )

            self.observability.finish_stage(
                execution_id,
                "ranking",
                attributes={
                    "items": len(ranked),
                },
            )

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.RANKING_COMPLETED,
                attributes={
                    "items": len(ranked),
                },
            )


            #
            # Selection Stage
            #

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.SELECTION_STARTED,
            )

            self.observability.start_stage(
                execution_id,
                "selection",
            )

            selected = self.selector.select(
                candidates=ranked,
                policy=self.selection_policy,
            )

            self.observability.finish_stage(
                execution_id,
                "selection",
                attributes={
                    "items": len(
                        selected.items
                    ),
                },
            )

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.SELECTION_COMPLETED,
                attributes={
                    "items": len(
                        selected.items
                    ),
                },
            )


            #
            # Assembly Stage
            #

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.ASSEMBLY_STARTED,
            )

            self.observability.start_stage(
                execution_id,
                "assembly",
            )

            assembled = self.assembler.assemble(
                selected_context=selected,
                user_input=query,
            )

            self.observability.finish_stage(
                execution_id,
                "assembly",
                attributes={
                    "tokens": getattr(
                        assembled,
                        "total_tokens",
                        0,
                    ),
                },
            )

            self.observability.record_event(
                execution_id,
                ContextRuntimeEvent.ASSEMBLY_COMPLETED,
            )


            #
            # Metrics
            #

            trace = self.observability._active_traces.get(
                execution_id
            )

            trace_id = getattr(
                trace,
                "trace_id",
                None,
            )

            if trace_id is not None:

                provider = (
                    self.observability.provider
                )

                if hasattr(
                    provider,
                    "update_metrics",
                ):
                    provider.update_metrics(
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
                        original_tokens=getattr(
                            assembled,
                            "total_tokens",
                            0,
                        ),
                    )


            self.observability.finish_trace(
                execution_id,
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
                    "execution_id": execution_id,
                },
            )

            return assembled


        except Exception:

            self.observability.finish_trace(
                execution_id,
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
```
