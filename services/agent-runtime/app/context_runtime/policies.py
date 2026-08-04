"""
Context Selection Policies

Defines configurable policies used by Context Selector.

The policy layer is separated from selection logic to allow
future selector strategies without changing the core pipeline.

Sprint:
    S4-007-003 Context Selector
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SelectionPolicy:
    """
    Configuration policy for context selection.

    Attributes:
        max_items:
            Maximum number of context candidates allowed.

        max_tokens:
            Maximum token budget allowed for selected contexts.

        min_score:
            Minimum ranking score threshold.
            Candidates below this score will be excluded.
    """

    max_items: int = 5

    max_tokens: int = 2000

    min_score: float = 0.0
