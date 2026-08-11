"""
Context Runtime Factory Tests

Sprint:
S4-011 Context Intelligence / Decision Boundary

Validates:

- default Context Runtime composition
- default dependency construction
- coordinator injection into the default retriever
- explicit dependency preservation
- observability runtime construction
- fresh runtime graph creation
- composition-only factory boundary
"""

from app.context_runtime.assembler import (
    ContextAssembler,
)
from app.context_runtime.coordinator import (
    ContextRuntimeCoordinator,
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
from app.context_runtime.policies import SelectionPolicy
from app.context_runtime.ranker import (
    ContextRanker,
)
from app.context_runtime.retriever import (
    ContextRetriever,
)
from app.context_runtime.selector import (
    ContextSelector,
)


class FakeCoordinator:
    """Minimal coordinator test double."""


class FakeRetriever:
    """Minimal retriever test double."""


class FakeRanker:
    """Minimal ranker test double."""


class FakeSelector:
    """Minimal selector test double."""


class FakeAssembler:
    """Minimal assembler test double."""


class FakeObservability:
    """Minimal observability test double."""


def test_factory_creates_context_runtime_integration():
    """Factory must create the runtime integration."""

    runtime = ContextRuntimeFactory().create()

    assert isinstance(
        runtime,
        ContextRuntimeIntegration,
    )


def test_factory_creates_default_pipeline_dependencies():
    """Factory must compose all default pipeline dependencies."""

    runtime = ContextRuntimeFactory().create()

    assert isinstance(
        runtime.retriever,
        ContextRetriever,
    )
    assert isinstance(
        runtime.ranker,
        ContextRanker,
    )
    assert isinstance(
        runtime.selector,
        ContextSelector,
    )
    assert isinstance(
        runtime.assembler,
        ContextAssembler,
    )


def test_factory_creates_observability_runtime():
    """Factory must create the default observability runtime."""

    runtime = ContextRuntimeFactory().create()

    assert isinstance(
        runtime.observability,
        ContextRuntimeObservabilityRuntime,
    )


def test_factory_composes_single_dependency_graph():
    """
    Factory must compose the runtime as one dependency graph.

    The default retriever must be connected to the default
    ContextRuntimeCoordinator.
    """

    runtime = ContextRuntimeFactory().create()

    assert runtime.retriever is not None
    assert runtime.ranker is not None
    assert runtime.selector is not None
    assert runtime.assembler is not None
    assert runtime.observability is not None

    assert isinstance(
        runtime.retriever._coordinator,
        ContextRuntimeCoordinator,
    )


def test_factory_creates_default_coordinator_for_retriever():
    """
    Default retriever must receive a runtime coordinator.

    This verifies the composition boundary between the factory,
    coordinator, and runtime retriever.
    """

    runtime = ContextRuntimeFactory().create()

    assert runtime.retriever is not None
    assert runtime.retriever._coordinator is not None
    assert isinstance(
        runtime.retriever._coordinator,
        ContextRuntimeCoordinator,
    )


def test_factory_passes_coordinator_to_default_retriever():
    """Coordinator must be injected into the default retriever."""

    coordinator = FakeCoordinator()

    runtime = ContextRuntimeFactory(
        coordinator=coordinator,
    ).create()

    assert runtime.retriever._coordinator is coordinator


def test_factory_preserves_explicit_coordinator():
    """Explicit coordinator must not be replaced by a default."""

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


def test_factory_creates_fresh_runtime_graph():
    """Each factory invocation must create independent defaults."""

    first = ContextRuntimeFactory().create()
    second = ContextRuntimeFactory().create()

    assert first is not second

    assert first.retriever is not second.retriever
    assert first.ranker is not second.ranker
    assert first.selector is not second.selector
    assert first.assembler is not second.assembler
    assert first.observability is not second.observability

    assert (
        first.retriever._coordinator
        is not second.retriever._coordinator
    )


def test_factory_does_not_execute_runtime_operations():
    """
    Factory construction must not execute runtime operations.

    Creating the runtime should only compose dependencies.
    """

    runtime = ContextRuntimeFactory().create()

    coordinator = runtime.retriever._coordinator

    assert coordinator.get_context() is None
