"""
Context Runtime Refresh Engine

Provides the default implementation of the ContextRefreshEngine
contract.

Sprint:
S4-011-006-002 Default Context Refresh Engine

Author:
OneMind Platform

License:
MIT
"""

from __future__ import annotations

from datetime import datetime, timezone

from app.context_runtime.interface import (
    ContextRefreshEngine,
)
from app.context_runtime.lifecycle import (
    DefaultContextLifecycleManager,
)
from app.context_runtime.models import (
    ContextLifecycle,
    ContextRefreshPolicy,
    ContextRuntimeState,
)


class DefaultContextRefreshEngine(ContextRefreshEngine):
    """
    Default context refresh engine.

    Responsibilities:
    - determine whether runtime context requires refresh
    - execute the lifecycle portion of refresh
    - update refresh timestamps

    This component intentionally does not:
    - retrieve context
    - rank context
    - select context
    - modify context content
    - perform relevance evaluation
    - invoke Agent Runtime
    """

    def __init__(
        self,
        policy: ContextRefreshPolicy | None = None,
    ) -> None:
        self.policy = (
            policy
            or ContextRefreshPolicy()
        )

        self._lifecycle_manager = (
            DefaultContextLifecycleManager()
        )

    def should_refresh(
        self,
        state: ContextRuntimeState,
    ) -> bool:
        """
        Determine whether runtime context requires refresh.

        Refresh rules:

        1. Disabled policy -> False
        2. ARCHIVED / REMOVED -> False
        3. STALE -> True
        4. No previous refresh -> compare created_at
           against max_age_seconds
        5. Existing refresh -> compare last_refresh
           against refresh_interval_seconds
        """

        if not self.policy.enabled:
            return False

        if state.lifecycle in (
            ContextLifecycle.ARCHIVED,
            ContextLifecycle.REMOVED,
        ):
            return False

        if state.lifecycle == ContextLifecycle.STALE:
            return True

        now = datetime.now(timezone.utc)

        if state.last_refresh is None:
            age = (
                now - state.created_at
            ).total_seconds()

            return (
                age >= self.policy.max_age_seconds
            )

        elapsed = (
            now - state.last_refresh
        ).total_seconds()

        if elapsed >= self.policy.max_age_seconds:
            return True

        return (
            elapsed
            >= self.policy.refresh_interval_seconds
        )

    def refresh(
        self,
        state: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        Execute the lifecycle portion of refresh.

        ACTIVE refresh:
            ACTIVE -> STALE -> ACTIVE

        STALE refresh:
            STALE -> ACTIVE

        The lifecycle transitions are delegated to the
        lifecycle manager rather than mutated directly.

        Context content itself is intentionally untouched.
        """

        if not self.should_refresh(state):
            return state

        now = datetime.now(timezone.utc)

        if state.lifecycle == ContextLifecycle.ACTIVE:
            state = self._lifecycle_manager.mark_stale(
                state
            )

        if state.lifecycle == ContextLifecycle.STALE:
            state = self._lifecycle_manager.activate(
                state
            )

        state.last_refresh = now
        state.updated_at = now

        return state
