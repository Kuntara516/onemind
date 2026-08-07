"""
Context Runtime Observability Provider Manager Tests

Sprint:
    S4-010-003 Provider Integration Layer
"""

from app.context_runtime.observability import (
    ContextObservabilityService,
    ObservabilityProviderManager,
)


def test_default_provider_is_memory():
    """
    Default provider should use in-memory service.
    """

    manager = ObservabilityProviderManager()

    provider = manager.get_provider()

    assert isinstance(
        provider,
        ContextObservabilityService,
    )


def test_explicit_memory_provider():
    """
    Memory provider selection.
    """

    manager = ObservabilityProviderManager(
        provider="memory",
    )

    provider = manager.get_provider()

    assert provider.__class__.__name__ == (
        "ContextObservabilityService"
    )


def test_invalid_provider_rejected():
    """
    Unknown provider should fail.
    """

    try:
        ObservabilityProviderManager(
            provider="unknown",
        )

    except ValueError as exc:
        assert (
            "Unsupported observability provider"
            in str(exc)
        )

    else:
        assert False, (
            "Expected ValueError"
        )
