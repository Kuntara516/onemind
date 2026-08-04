from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.context_runtime.models import (
    ContextBudget,
    ContextRuntimeState,
)


class ContextRuntimeManager(ABC):
    """
    Contract for managing runtime context lifecycle.
    """

    @abstractmethod
    def initialize(
        self,
        state: ContextRuntimeState,
    ) -> None:
        """
        Initialize active runtime context.
        """
        raise NotImplementedError

    @abstractmethod
    def get_state(
        self,
    ) -> Optional[ContextRuntimeState]:
        """
        Return current runtime state.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        state: ContextRuntimeState,
    ) -> None:
        """
        Update runtime context state.
        """
        raise NotImplementedError


class ContextBudgetManager(ABC):
    """
    Contract for context token budget management.
    """

    @abstractmethod
    def allocate(
        self,
        budget: ContextBudget,
    ) -> ContextBudget:
        raise NotImplementedError

    @abstractmethod
    def consume(
        self,
        tokens: int,
    ) -> ContextBudget:
        raise NotImplementedError

    @abstractmethod
    def remaining(
        self,
    ) -> int:
        raise NotImplementedError


class ContextLifecycleManager(ABC):
    """
    Contract for context lifecycle transitions.
    """

    @abstractmethod
    def activate(
        self,
        state: ContextRuntimeState,
    ) -> ContextRuntimeState:
        raise NotImplementedError

    @abstractmethod
    def mark_stale(
        self,
        state: ContextRuntimeState,
    ) -> ContextRuntimeState:
        raise NotImplementedError

    @abstractmethod
    def archive(
        self,
        state: ContextRuntimeState,
    ) -> ContextRuntimeState:
        raise NotImplementedError


class ContextRefreshEngine(ABC):
    """
    Contract for context refresh decision and execution.
    """

    @abstractmethod
    def should_refresh(
        self,
        state: ContextRuntimeState,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def refresh(
        self,
        state: ContextRuntimeState,
    ) -> ContextRuntimeState:
        raise NotImplementedError
