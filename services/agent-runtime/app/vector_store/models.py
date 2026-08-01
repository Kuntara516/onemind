from typing import Any

from pydantic import BaseModel, Field


class VectorRecord(BaseModel):
    """
    Storage-independent vector record model.
    """

    id: str
    collection: str = "default"
    vector: list[float]
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)