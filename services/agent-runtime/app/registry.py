from typing import Dict


class AgentRegistry:
    """
    Registry for managing OneMind agents.
    """

    def __init__(self):
        self.agents: Dict[str, object] = {}


    def register(self, agent):
        """
        Register an agent instance.
        """

        self.agents[agent.name] = agent


    def unregister(self, name: str):
        """
        Remove agent from registry.
        """

        if name in self.agents:
            del self.agents[name]


    def get(self, name: str):
        """
        Retrieve agent by name.
        """

        return self.agents.get(name)


    def has(self, name: str) -> bool:
        """
        Check agent existence.
        """

        return name in self.agents


    def list_agents(self):
        """
        List available agents.
        """

        return [
            {
                "name": agent.name,
                "description": getattr(
                    agent,
                    "description",
                    ""
                )
            }
            for agent in self.agents.values()
        ]


registry = AgentRegistry()