from typing import Dict, Any


class AgentContext:
    """
    Runtime context shared across agents.
    """

    def __init__(
        self,
        agent_id: str,
        request_id: str,
        metadata: Dict[str, Any] | None = None
    ):
        self.agent_id = agent_id
        self.request_id = request_id
        self.metadata = metadata or {}


    def get(self, key: str, default=None):
        return self.metadata.get(key, default)


    def set(self, key: str, value):
        self.metadata[key] = value