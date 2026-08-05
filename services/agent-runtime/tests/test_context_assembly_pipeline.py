"""
Context Assembly Pipeline Tests

Sprint:
    S4-007-004 Context Assembly

Validates full pipeline:

ContextCandidate[]
        |
        v
DefaultContextRanker
        |
        v
DefaultContextSelector
        |
        v
DefaultContextAssembler
        |
        v
AssembledContext
"""

from app.context_runtime.assembly_models import (
    PromptSectionType,
)

from app.context_runtime.assembler import (
    DefaultContextAssembler,
)

from app.context_runtime.models import (
    ContextCandidate,
    ContextLifecycle,
)

from app.context_runtime.ranker import (
    DefaultContextRanker,
)

from app.context_runtime.selector import (
    DefaultContextSelector,
)

from app.context_runtime.policies import (
    SelectionPolicy,
)


def create_candidate(
    context_id: str,
    content: str,
    score: float,
) -> ContextCandidate:
    """
    Create pipeline candidate helper.
    """

    return ContextCandidate(
        context_id=context_id,
        content=content,
        score=score,
        lifecycle=ContextLifecycle.ACTIVE,
        metadata={
            "source": "test",
        },
    )


def test_full_rank_select_assemble_pipeline():
    """
    Ranked candidates should flow through
    selector and assembler.
    """

    candidates = [
        create_candidate(
            "memory-a",
            "important memory",
            0.95,
        ),
        create_candidate(
            "memory-b",
            "secondary memory",
            0.80,
        ),
        create_candidate(
            "memory-c",
            "low value memory",
            0.30,
        ),
    ]

    ranked = DefaultContextRanker().rank(
        candidates=candidates,
        query="important",
    )

    selected = DefaultContextSelector().select(
        ranked,
        SelectionPolicy(
            min_score=0.5,
            max_items=2,
        ),
    )

    result = DefaultContextAssembler().assemble(
        selected_context=selected,
        system_prompt="You are OneMind.",
        user_input="Recall my memory.",
    )

    assert result.section_count == 4

    assert (
        result.sections[0].section_type
        == PromptSectionType.SYSTEM
    )

    assert (
        result.sections[-1].section_type
        == PromptSectionType.USER
    )


def test_pipeline_preserves_selected_memory():
    """
    Selected memory should reach final assembly.
    """

    candidates = [
        create_candidate(
            "memory-1",
            "user likes Python",
            0.95,
        ),
        create_candidate(
            "memory-2",
            "user likes coffee",
            0.85,
        ),
    ]

    ranked = DefaultContextRanker().rank(
        candidates=candidates,
        query="Python",
    )

    selected = DefaultContextSelector().select(
        ranked,
        SelectionPolicy(
            max_items=2,
        ),
    )

    result = DefaultContextAssembler().assemble(
        selected_context=selected,
    )

    memory_sections = [
        section
        for section in result.sections
        if section.section_type
        == PromptSectionType.MEMORY
    ]

    assert len(memory_sections) == 2

    assert (
        memory_sections[0]
        .metadata["context_id"]
        == "memory-1"
    )


def test_pipeline_preserves_token_accounting():
    """
    Token accounting should survive the
    complete pipeline.
    """

    candidates = [
        create_candidate(
            "large-memory",
            "one two three four five",
            0.90,
        )
    ]

    ranked = DefaultContextRanker().rank(
        candidates=candidates,
        query="memory",
    )

    selected = DefaultContextSelector().select(
        ranked,
        SelectionPolicy(
            max_items=1,
        ),
    )

    result = DefaultContextAssembler().assemble(
        selected_context=selected,
    )

    assert result.total_tokens == 5


def test_pipeline_returns_trace_metadata():
    """
    Final assembled context should expose
    pipeline metadata.
    """

    selected = DefaultContextSelector().select(
        [
            create_candidate(
                "trace-memory",
                "trace context",
                0.9,
            )
        ],
        SelectionPolicy(),
    )

    result = DefaultContextAssembler().assemble(
        selected_context=selected,
    )

    assert (
        result.metadata["assembler"]
        == "default"
    )

    assert (
        result.metadata["selected_items"]
        == 1
    )

    assert (
        result.metadata["assembled_sections"]
        == 1
    )
