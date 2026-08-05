"""
Context Assembly Models

Sprint:
    S4-007-004 Context Assembly

Defines the final prompt assembly models that bridge
Context Intelligence and Agent Runtime.
"""

from enum import Enum

from pydantic import BaseModel, Field


class PromptSectionType(str, Enum):
    """
    Supported prompt section types.
    """

    SYSTEM = "system"

    MEMORY = "memory"

    KNOWLEDGE = "knowledge"

    CONVERSATION = "conversation"

    USER = "user"


class PromptSection(BaseModel):
    """
    Represents one logical prompt section.

    Each section remains independent until the
    prompt rendering stage.
    """

    section_type: PromptSectionType

    content: str

    token_count: int = 0

    metadata: dict[str, object] = Field(
        default_factory=dict
    )


class AssembledContext(BaseModel):
    """
    Final context package produced by the
    Context Assembly layer.

    This object is passed to Agent Runtime
    before prompt rendering.
    """

    sections: list[PromptSection] = Field(
        default_factory=list
    )

    total_tokens: int = 0

    metadata: dict[str, object] = Field(
        default_factory=dict
    )

    @property
    def section_count(self) -> int:
        """
        Number of assembled prompt sections.
        """
        return len(self.sections)

    def add_section(
        self,
        section: PromptSection,
    ) -> None:
        """
        Append a prompt section and update the
        total token count.
        """

        self.sections.append(section)

        self.total_tokens += section.token_count

    def get_sections(
        self,
        section_type: PromptSectionType,
    ) -> list[PromptSection]:
        """
        Return all sections of the requested type.
        """

        return [
            section
            for section in self.sections
            if section.section_type == section_type
        ]

