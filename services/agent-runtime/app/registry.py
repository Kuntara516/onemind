from typing import Dict


class AgentRegistry:

    def __init__(self):
        self.agents: Dict[str, object] = {}

    def register(self, agent):
        self.agents[agent.name] = agent

    def get(self, name: str):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())


registry = AgentRegistry()