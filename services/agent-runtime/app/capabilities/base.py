from abc import ABC, abstractmethod
from typing import Any


class BaseCapability(ABC):
    """
    Base interface for all OneMind capabilities.
    """

    name: str = ""

    @abstractmethod
    async def execute(self, **kwargs: Any) -> dict:
        """
        Execute capability logic.

        Args:
            **kwargs: Capability execution parameters.

        Returns:
            dict: Capability execution result.
        """
        raise NotImplementedError