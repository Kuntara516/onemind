"""
Context Runtime Integration

Sprint:
    S4-008 Context Runtime Integration

Bridges Context Intelligence pipeline
with Agent Runtime execution context.
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
    """

    def __init__(
        self,
        retriever: ContextRetriever,
        ranker: ContextRanker,
        selector: ContextSelector,
        assembler: ContextAssembler,
        selection_policy: SelectionPolicy | None = None,
    ):
        self.retriever = retriever
        self.ranker = ranker
        self.selector = selector
        self.assembler = assembler

        self.selection_policy = (
            selection_policy
            or SelectionPolicy()
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

        query = self._build_query(
            task
        )

        candidates = self.retriever.retrieve(
            query=query,
        )

        ranked = self.ranker.rank(
            candidates=candidates,
            query=query,
        )

        selected = self.selector.select(
            candidates=ranked,
            policy=self.selection_policy,
        )

        assembled = self.assembler.assemble(
            selected_context=selected,
            user_input=query,
        )

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

        return assembled


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
