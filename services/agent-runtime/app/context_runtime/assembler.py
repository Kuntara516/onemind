"""
Context Assembler

Sprint:
    S4-007-004 Context Assembly

Responsible for assembling the final context package
consumed by Agent Runtime.
"""

from abc import ABC, abstractmethod

from .assembly_models import (
    AssembledContext,
    PromptSection,
    PromptSectionType,
)
from .models import SelectedContext


class ContextAssembler(ABC):
    """
    Abstract interface for assembling runtime context.
    """

    @abstractmethod
    def assemble(
        self,
        selected_context: SelectedContext,
        system_prompt: str = "",
        conversation: str = "",
        user_input: str = "",
    ) -> AssembledContext:
        """
        Assemble the final runtime context.
        """
        raise NotImplementedError


class DefaultContextAssembler(ContextAssembler):
    """
    Default deterministic context assembler.

    Responsibilities:

    - preserve context ordering
    - assemble prompt sections
    - calculate total token count
    """

    def assemble(
        self,
        selected_context: SelectedContext,
        system_prompt: str = "",
        conversation: str = "",
        user_input: str = "",
    ) -> AssembledContext:
        """
        Assemble all prompt sections into a single
        AssembledContext object.
        """

        assembled = AssembledContext(
            metadata={
                "assembler": "default",
            }
        )

        #
        # System Prompt
        #
        if system_prompt:

            assembled.add_section(
                PromptSection(
                    section_type=PromptSectionType.SYSTEM,
                    content=system_prompt,
                    token_count=self._estimate_tokens(
                        system_prompt
                    ),
                )
            )

        #
        # Selected Context
        #
        for candidate in selected_context.items:

            assembled.add_section(
                PromptSection(
                    section_type=PromptSectionType.MEMORY,
                    content=candidate.content or "",
                    token_count=self._estimate_tokens(
                        candidate.content or ""
                    ),
                    metadata={
                        "context_id": candidate.context_id,
                        "score": candidate.score,
                    },
                )
            )

        #
        # Conversation
        #
        if conversation:

            assembled.add_section(
                PromptSection(
                    section_type=PromptSectionType.CONVERSATION,
                    content=conversation,
                    token_count=self._estimate_tokens(
                        conversation
                    ),
                )
            )

        #
        # User Input
        #
        if user_input:

            assembled.add_section(
                PromptSection(
                    section_type=PromptSectionType.USER,
                    content=user_input,
                    token_count=self._estimate_tokens(
                        user_input
                    ),
                )
            )

        assembled.metadata.update(
            {
                "selected_items": len(
                    selected_context.items
                ),
                "assembled_sections": assembled.section_count,
            }
        )

        return assembled

    @staticmethod
    def _estimate_tokens(
        text: str,
    ) -> int:
        """
        Lightweight token estimation.

        Current implementation uses a simple
        whitespace-based approximation.

        Future versions should integrate the
        production tokenizer.
        """

        if not text.strip():
            return 0

        return len(text.split())

