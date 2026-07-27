from pydantic import BaseModel
from typing import Any


class AgentTask(BaseModel):
    agent: str
    task: dict[str, Any]


class AgentResult(BaseModel):
    agent: str
    status: str
    result: Any