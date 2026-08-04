"""
Default Context Compression Strategy.

Provides deterministic compression logic
for the Context Compression Layer.

Sprint 4 - Context Intelligence & Retrieval Pipeline
"""

from ..models import CompressionRequest, CompressionResult, CompressionCandidate


class DefaultContextCompressionStrategy:
    """
    Default compression strategy implementation.

    Strategy principles:

    - keep high priority candidates first
    - respect token budget when provided
    - preserve deterministic behavior
    - avoid losing important context
    """

    async def compress(
        self,
        request: CompressionRequest,
    ) -> CompressionResult:
        """
        Compress context candidates.

        Algorithm:

        1. Sort candidates by priority score descending.
        2. Keep candidates until token budget is reached.
        3. Return retained candidates with metrics.
        """

        candidates = sorted(
            request.candidates,
            key=lambda item: item.priority_score,
            reverse=True,
        )

        selected: list[CompressionCandidate] = []

        original_token_count = sum(
            item.estimated_tokens
            for item in candidates
        )

        current_tokens = 0

        for candidate in candidates:
            if request.token_budget is not None:
                if (
                    current_tokens + candidate.estimated_tokens
                    > request.token_budget
                ):
                    continue

            selected.append(candidate)

            current_tokens += candidate.estimated_tokens

        removed_candidates = (
            len(candidates) - len(selected)
        )

        return CompressionResult(
            compressed_candidates=selected,
            original_token_count=original_token_count,
            compressed_token_count=current_tokens,
            removed_candidates=removed_candidates,
            metadata={
                "strategy": "default",
                "policy": request.compression_policy,
            },
        )
