"""
Context Runtime Factory

Sprint:
S4-011 Context Intelligence / Decision Boundary

Responsibilities:

- compose the default Context Runtime pipeline
- provide explicit dependency injection boundaries
- keep construction separate from runtime execution

The factory is intentionally composition-only. It must not execute
context retrieval, evaluation, decision, refresh, or agent execution.
"""

from __future__ import annotations

from typing import Any

from .assembler import (
    ContextAssembler,
    DefaultContextAssembler,
)
from .coordinator import ContextRuntimeCoordinator
from .integration import ContextRuntimeIntegration
from .observability.runtime import ContextRuntimeObservabilityRuntime
from .policies import SelectionPolicy
from .ranker import (
    ContextRanker,
    DefaultContextRanker,
)
from .retriever import (
    ContextRetriever,
    DefaultContextRetriever,
)
from .selector import (
    ContextSelector,
    DefaultContextSelector,
)


class ContextRuntimeFactory:
    """
    Composition factory for Context Runtime.

    The factory owns construction only. Runtime behavior remains inside
    ContextRuntimeIntegration and its injected collaborators.

    Dependencies may be supplied explicitly for tests or alternative
    implementations. Missing pipeline components receive the default
    deterministic implementations.
    """

    def __init__(
        self,
        *,
        coordinator: Any | None = None,
        retriever: ContextRetriever | None = None,
        ranker: ContextRanker | None = None,
        selector: ContextSelector | None = None,
        assembler: ContextAssembler | None = None,
        selection_policy: SelectionPolicy | None = None,
        observability: ContextRuntimeObservabilityRuntime | None = None,
    ) -> None:
        self.coordinator = (
            coordinator
            if coordinator is not None
            else ContextRuntimeCoordinator()
        )
        self.retriever = retriever
        self.ranker = ranker
        self.selector = selector
        self.assembler = assembler
        self.selection_policy = selection_policy
        self.observability = observability

    def create(self) -> ContextRuntimeIntegration:
        """
        Create a fully composed Context Runtime integration.

        Construction only:
        no retrieval, evaluation, decision, refresh, or execution
        is performed here.
        """

        retriever = self.retriever or DefaultContextRetriever(
            coordinator=self.coordinator,
        )
        ranker = self.ranker or DefaultContextRanker()
        selector = self.selector or DefaultContextSelector()
        assembler = self.assembler or DefaultContextAssembler()
        selection_policy = self.selection_policy or SelectionPolicy()
        observability = (
            self.observability
            or ContextRuntimeObservabilityRuntime()
        )

        return ContextRuntimeIntegration(
            retriever=retriever,
            ranker=ranker,
            selector=selector,
            assembler=assembler,
            selection_policy=selection_policy,
            observability=observability,
        )
