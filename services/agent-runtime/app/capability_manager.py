from typing import Any

from .capabilities import (
    BaseCapability,
    CapabilityRegistry,
    EchoCapability,
)


class CapabilityManager:
    """
    Service layer responsible for managing
    OneMind capabilities.
    """

    def __init__(
        self,
        registry: CapabilityRegistry | None = None,
    ):
        self.registry = registry or CapabilityRegistry()

        self.register_default_capabilities()

    def register_default_capabilities(
        self,
    ) -> None:
        """
        Register built-in OneMind capabilities.
        """

        self.register(
            EchoCapability()
        )

    def register(
        self,
        capability: BaseCapability,
    ) -> None:
        """
        Register a capability.
        """

        self.registry.register(capability)

    async def execute(
        self,
        capability_name: str,
        **kwargs: Any,
    ) -> dict:
        """
        Execute a capability by name.
        """

        capability = self.registry.get(
            capability_name
        )

        if capability is None:
            raise ValueError(
                f"Capability not found: {capability_name}"
            )

        return await capability.execute(
            **kwargs
        )

    def list_capabilities(self) -> list[str]:
        """
        Return available capability names.
        """

        return self.registry.list()