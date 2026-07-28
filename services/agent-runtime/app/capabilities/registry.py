from typing import Optional

from .base import BaseCapability


class CapabilityRegistry:
    """
    Registry responsible for managing OneMind capabilities.
    """

    def __init__(self):
        self._capabilities: dict[str, BaseCapability] = {}

    def register(
        self,
        capability: BaseCapability
    ) -> None:
        """
        Register a capability.

        Args:
            capability: Capability instance.
        """
        self._capabilities[capability.name] = capability

    def get(
        self,
        name: str
    ) -> Optional[BaseCapability]:
        """
        Retrieve capability by name.

        Args:
            name: Capability name.

        Returns:
            Capability instance or None.
        """
        return self._capabilities.get(name)

    def list(self) -> list[str]:
        """
        List registered capability names.

        Returns:
            List of capability names.
        """
        return list(self._capabilities.keys())