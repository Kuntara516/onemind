from typing import Any

from .base import BaseCapability


class EchoCapability(BaseCapability):
    """
    Simple echo capability for testing OneMind capability framework.
    """

    name = "echo"

    async def execute(self, **kwargs: Any) -> dict:
        """
        Echo input text.

        Args:
            **kwargs: Capability execution parameters.

        Returns:
            dict: Echo result.
        """

        text = kwargs.get("text", "")

        return {
            "echo": text
        }