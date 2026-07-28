from enum import Enum


class TaskStatus(str, Enum):
    """
    Agent task lifecycle status.

    Lifecycle:

    CREATED
        |
        v
    QUEUED
        |
        v
    RUNNING
        |
        +----------+
        |          |
        v          v
    COMPLETED    FAILED
    """

    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"