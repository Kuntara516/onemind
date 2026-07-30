from abc import ABC, abstractmethod

from .trace import ExecutionTrace


class TraceRecorder(ABC):
    """
    Abstract interface for execution trace storage.
    """

    @abstractmethod
    def record(
        self,
        trace: ExecutionTrace,
    ):
        """
        Store execution trace.
        """
        pass

    @abstractmethod
    def get(
        self,
        trace_id: str,
    ) -> ExecutionTrace | None:
        """
        Retrieve trace by identifier.
        """
        pass

    @abstractmethod
    def list(
        self,
    ) -> list[ExecutionTrace]:
        """
        List all stored traces.
        """
        pass

    @abstractmethod
    def clear(
        self,
    ):
        """
        Remove all traces.
        """
        pass


class InMemoryTraceRecorder(TraceRecorder):
    """
    In-memory execution trace recorder.

    Initial trace storage implementation
    for Agent Runtime.
    """

    def __init__(self):
        self.traces: dict[str, ExecutionTrace] = {}

    def record(
        self,
        trace: ExecutionTrace,
    ):
        self.traces[trace.trace_id] = trace

    def get(
        self,
        trace_id: str,
    ) -> ExecutionTrace | None:
        return self.traces.get(trace_id)

    def list(
        self,
    ) -> list[ExecutionTrace]:
        return list(self.traces.values())

    def clear(
        self,
    ):
        self.traces.clear()