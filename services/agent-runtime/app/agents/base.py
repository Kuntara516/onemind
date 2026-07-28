from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base interface for all OneMind agents.

    Every agent must implement execute()
    with Runtime Context and Capability injection.
    """

    name: str = "unknown-agent"
    description: str = ""


    @abstractmethod
    async def execute(
        self,
        task: dict,
        context,
        capabilities
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