from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base interface for all OneMind agents.
    """

    name: str = "unknown-agent"
    description: str = ""


    @abstractmethod
    async def execute(self,task: dict, context=None) -> dict:
        """
        Execute agent task.

        Args:
            task: Agent input payload

        Returns:
            Agent execution result
        """
        pass