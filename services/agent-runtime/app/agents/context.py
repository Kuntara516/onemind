from typing import Dict, Any


class AgentContext:
    """
    Runtime context shared across agents.

    AgentContext represents execution state
    that flows through the Agent Runtime lifecycle.
    """

    def __init__(
        self,
        request_id: str,
        session_id: str | None = None,
        user_id: str | None = None,
        metadata: Dict[str, Any] | None = None
    ):
        self.request_id = request_id
        self.session_id = session_id
        self.user_id = user_id
        self.metadata = metadata or {}


    def get(
        self,
        key: str,
        default=None
    ):
        """
        Retrieve metadata value.
        """

        return self.metadata.get(
            key,
            default
        )


    def set(
        self,
        key: str,
        value
    ):
        """
        Store metadata value.
        """

        self.metadata[key] = value