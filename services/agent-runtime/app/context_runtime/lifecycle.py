from __future__ import annotations

from app.context_runtime.interface import (
    ContextLifecycleManager,
)

from app.context_runtime.models import (
    ContextLifecycle,
    ContextRuntimeState,
)


class DefaultContextLifecycleManager(
    ContextLifecycleManager
):
    """
    Default lifecycle manager.

    Responsible for enforcing valid
    context lifecycle transitions.
    """

    def activate(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        CREATED -> ACTIVE

        Idempotent:
        ACTIVE -> ACTIVE
        """

        if context.lifecycle == (
            ContextLifecycle.ACTIVE
        ):
            return context

        if context.lifecycle != (
            ContextLifecycle.CREATED
        ):
            raise ValueError(
                "Only CREATED context can be activated"
            )

        context.lifecycle = (
            ContextLifecycle.ACTIVE
        )

        return context

    def mark_stale(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        ACTIVE -> STALE
        """

        if context.lifecycle != (
            ContextLifecycle.ACTIVE
        ):
            raise ValueError(
                "Only ACTIVE context can become stale"
            )

        context.lifecycle = (
            ContextLifecycle.STALE
        )

        return context

    def archive(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        ACTIVE/STALE -> ARCHIVED
        """

        if context.lifecycle not in (
            ContextLifecycle.ACTIVE,
            ContextLifecycle.STALE,
        ):
            raise ValueError(
                "Only ACTIVE or STALE context can be archived"
            )

        context.lifecycle = (
            ContextLifecycle.ARCHIVED
        )

        return context

    def remove(
        self,
        context: ContextRuntimeState,
    ) -> ContextRuntimeState:
        """
        ARCHIVED -> REMOVED
        """

        if context.lifecycle != (
            ContextLifecycle.ARCHIVED
        ):
            raise ValueError(
                "Only ARCHIVED context can be removed"
            )

        context.lifecycle = (
            ContextLifecycle.REMOVED
        )

        return context
