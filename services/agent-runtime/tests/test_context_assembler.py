"""
Context Assembler Tests

Sprint:
    S4-007-004 Context Assembly

Validates:

SelectedContext
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
    SelectedContext,
)


def create_candidate(
    context_id: str,
    content: str,
    score: float = 0.0,
) -> ContextCandidate:
    """
    Create context candidate helper.
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


def create_selected_context(
    candidates: list[ContextCandidate],
) -> SelectedContext:
    """
    Create SelectedContext helper.
    """

    return SelectedContext(
        items=candidates,
        total_tokens=0,
        total_score=0.0,
        metadata={
            "selector": "test",
        },
    )


def test_assemble_system_prompt():
    """
    Assembler should create system section.
    """

    assembler = DefaultContextAssembler()

    result = assembler.assemble(
        selected_context=create_selected_context([]),
        system_prompt="You are OneMind agent.",
    )

    assert result.section_count == 1

    assert (
        result.sections[0].section_type
        == PromptSectionType.SYSTEM
    )

    assert (
        result.sections[0].content
        == "You are OneMind agent."
    )


def test_assemble_selected_memory_context():
    """
    Selected context should become memory sections.
    """

    assembler = DefaultContextAssembler()

    selected_context = create_selected_context(
        [
            create_candidate(
                "memory-1",
                "User prefers concise answers.",
                0.9,
            ),
            create_candidate(
                "memory-2",
                "User uses Python.",
                0.8,
            ),
        ]
    )

    result = assembler.assemble(
        selected_context=selected_context,
    )

    assert result.section_count == 2

    assert all(
        section.section_type
        == PromptSectionType.MEMORY
        for section in result.sections
    )

    assert (
        result.sections[0]
        .metadata["context_id"]
        == "memory-1"
    )


def test_assemble_conversation_and_user_input():
    """
    Conversation and user input should become
    separate sections.
    """

    assembler = DefaultContextAssembler()

    result = assembler.assemble(
        selected_context=create_selected_context([]),
        conversation="Previous conversation",
        user_input="Current question",
    )

    section_types = [
        section.section_type
        for section in result.sections
    ]

    assert section_types == [
        PromptSectionType.CONVERSATION,
        PromptSectionType.USER,
    ]


def test_calculate_total_tokens():
    """
    Total token count should be accumulated
    from all sections.
    """

    assembler = DefaultContextAssembler()

    result = assembler.assemble(
        selected_context=create_selected_context([]),
        system_prompt="one two three",
        user_input="four five",
    )

    assert result.total_tokens == 5


def test_preserve_section_order():
    """
    Assembler should preserve logical section order.
    """

    assembler = DefaultContextAssembler()

    result = assembler.assemble(
        selected_context=create_selected_context(
            [
                create_candidate(
                    "memory-1",
                    "memory content",
                )
            ]
        ),
        system_prompt="system",
        conversation="conversation",
        user_input="user",
    )

    section_types = [
        section.section_type
        for section in result.sections
    ]

    assert section_types == [
        PromptSectionType.SYSTEM,
        PromptSectionType.MEMORY,
        PromptSectionType.CONVERSATION,
        PromptSectionType.USER,
    ]


def test_return_assembly_metadata():
    """
    Assembler should expose metadata.
    """

    assembler = DefaultContextAssembler()

    result = assembler.assemble(
        selected_context=create_selected_context(
            [
                create_candidate(
                    "memory-1",
                    "context",
                )
            ]
        ),
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

