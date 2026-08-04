from __future__ import annotations

from app.context_runtime.interface import (
    ContextLifecycleManager,
)
from app.context_runtime.models import (
    ContextLifecycle,
    ContextRuntimeState,
)


class DefaultContextLifecycleManager(ContextLifecycleManager):
    """
    Default implementation for context lifecycle management.
    """

    def activate(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        Activate context runtime.
        """

        if context.lifecycle == ContextLifecycle.REMOVED:
            raise ValueError(
                "Removed context cannot be activated"
            )

        context.lifecycle = ContextLifecycle.ACTIVE

        return context

    def mark_stale(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        Mark context as stale.
        """

        if context.lifecycle != ContextLifecycle.ACTIVE:
            raise ValueError(
                "Only active context can become stale"
            )

        context.lifecycle = ContextLifecycle.STALE

        return context

    def archive(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        Archive context runtime.
        """

        if context.lifecycle not in (
            ContextLifecycle.ACTIVE,
            ContextLifecycle.STALE,
        ):
            raise ValueError(
                "Only active or stale context can be archived"
            )

        context.lifecycle = ContextLifecycle.ARCHIVED

        return context

    def remove(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        Remove context runtime.
        """

        if context.lifecycle != ContextLifecycle.ARCHIVED:
            raise ValueError(
                "Only archived context can be removed"
            )

        context.lifecycle = ContextLifecycle.REMOVED

        return context
