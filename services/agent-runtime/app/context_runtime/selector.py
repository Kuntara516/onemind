"""
Context Selector

Responsible for selecting final context items from ranked candidates.

Sprint:
    S4-007-003 Context Selector
"""

from __future__ import annotations

from typing import Iterable

from .models import ContextCandidate, SelectedContext
from .policies import SelectionPolicy


class ContextSelector:
    """
    Base interface for context selection.

    Selector receives already ranked candidates and decides
    which candidates should enter the final context package.
    """

    def select(
        self,
        candidates: Iterable[ContextCandidate],
        policy: SelectionPolicy,
    ) -> SelectedContext:
        raise NotImplementedError


class DefaultContextSelector(ContextSelector):
    """
    Default greedy context selector.

    Selection strategy:
        1. Preserve ranking order.
        2. Remove candidates below min_score.
        3. Respect max_items.
        4. Respect max_tokens.

    The selector does not modify candidate scores.
    """

    def select(
        self,
        candidates: Iterable[ContextCandidate],
        policy: SelectionPolicy,
    ) -> SelectedContext:

        selected: list[ContextCandidate] = []
        total_tokens = 0
        total_score = 0.0

        for candidate in candidates:

            if candidate.score < policy.min_score:
                continue

            if len(selected) >= policy.max_items:
                break

            candidate_tokens = self._estimate_tokens(candidate)

            if (
                total_tokens + candidate_tokens
                > policy.max_tokens
            ):
                break

            selected.append(candidate)

            total_tokens += candidate_tokens
            total_score += candidate.score

        return SelectedContext(
            items=selected,
            total_tokens=total_tokens,
            total_score=total_score,
            metadata={
                "selector": "default",
                "max_items": policy.max_items,
                "max_tokens": policy.max_tokens,
                "min_score": policy.min_score,
            },
        )

    @staticmethod
    def _estimate_tokens(
        candidate: ContextCandidate,
    ) -> int:
        """
        Estimate token usage.

        Temporary approximation:
            1 token ~= 4 characters

        Replace with real tokenizer integration
        when LLM context accounting is introduced.
        """

        if not candidate.content:
            return 0

        return max(
            1,
            len(candidate.content) // 4,
        )
