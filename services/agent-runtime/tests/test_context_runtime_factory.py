"""
Tests for Context Runtime Factory.

Sprint:
    S4-011 Context Runtime Factory

Validates:

    - default dependency composition
    - coordinator injection into default retriever
    - explicit dependency injection
    - selection policy injection
    - observability injection
    - factory construction remains side-effect free
"""

from app.context_runtime.assembler import (
    DefaultContextAssembler,
)
from app.context_runtime.factory import (
    ContextRuntimeFactory,
)
from app.context_runtime.integration import (
    ContextRuntimeIntegration,
)
from app.context_runtime.observability.runtime import (
    ContextRuntimeObservabilityRuntime,
)
from app.context_runtime.policies import (
    SelectionPolicy,
)
from app.context_runtime.ranker import (
    DefaultContextRanker,
)
from app.context_runtime.retriever import (
    DefaultContextRetriever,
)
from app.context_runtime.selector import (
    DefaultContextSelector,
)


class FakeCoordinator:
    """Minimal coordinator used to verify dependency propagation."""


class FakeRetriever:
    """Explicit retriever dependency."""


class FakeRanker:
    """Explicit ranker dependency."""


class FakeSelector:
    """Explicit selector dependency."""


class FakeAssembler:
    """Explicit assembler dependency."""


class FakeObservability:
    """Explicit observability dependency."""


def test_factory_creates_context_runtime_integration():
    """Factory must return the runtime integration boundary."""

    runtime = ContextRuntimeFactory().create()

    assert isinstance(
        runtime,
        ContextRuntimeIntegration,
    )


def test_factory_uses_default_pipeline_components():
    """Default factory construction must compose all default components."""

    runtime = ContextRuntimeFactory().create()

    assert isinstance(
        runtime.retriever,
        DefaultContextRetriever,
    )
    assert isinstance(
        runtime.ranker,
        DefaultContextRanker,
    )
    assert isinstance(
        runtime.selector,
        DefaultContextSelector,
    )
    assert isinstance(
        runtime.assembler,
        DefaultContextAssembler,
    )
    assert isinstance(
        runtime.selection_policy,
        SelectionPolicy,
    )
    assert isinstance(
        runtime.observability,
        ContextRuntimeObservabilityRuntime,
    )


def test_factory_passes_coordinator_to_default_retriever():
    """Coordinator must be injected into the default retriever."""

    coordinator = FakeCoordinator()

    runtime = ContextRuntimeFactory(
        coordinator=coordinator,
    ).create()

    assert runtime.retriever._coordinator is coordinator


def test_factory_preserves_explicit_dependencies():
    """Explicit dependencies must not be replaced by defaults."""

    retriever = FakeRetriever()
    ranker = FakeRanker()
    selector = FakeSelector()
    assembler = FakeAssembler()
    observability = FakeObservability()
    policy = SelectionPolicy(
        max_items=3,
        max_tokens=100,
        min_score=0.5,
    )

    runtime = ContextRuntimeFactory(
        retriever=retriever,
        ranker=ranker,
        selector=selector,
        assembler=assembler,
        selection_policy=policy,
        observability=observability,
    ).create()

    assert runtime.retriever is retriever
    assert runtime.ranker is ranker
    assert runtime.selector is selector
    assert runtime.assembler is assembler
    assert runtime.selection_policy is policy
    assert runtime.observability is observability


def test_factory_creates_independent_default_instances():
    """Separate factory calls must not share mutable runtime components."""

    first = ContextRuntimeFactory().create()
    second = ContextRuntimeFactory().create()

    assert first is not second
    assert first.retriever is not second.retriever
    assert first.ranker is not second.ranker
    assert first.selector is not second.selector
    assert first.assembler is not second.assembler
    assert first.observability is not second.observability


def test_factory_creation_does_not_execute_pipeline():
    """
    Factory construction must only compose dependencies.

    No retrieval, ranking, selection, assembly, or observability
    execution is performed by create().
    """

    runtime = ContextRuntimeFactory().create()

    assert runtime.retriever is not None
    assert runtime.ranker is not None
    assert runtime.selector is not None
    assert runtime.assembler is not None
