from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base interface for all OneMind agents.

    Every agent must implement execute()
    with Runtime Context injection.
    """

    name: str = "unknown-agent"
    description: str = ""


    @abstractmethod
    async def execute(
        self,
        task: dict,
        context
    ) -> dict:
        """
        Execute agent task.

        Args:
            task:
                Agent input payload

            context:
                Runtime execution context
                provided by AgentRuntime

        Returns:
            Agent execution result
        """

        pass