"""
Context Runtime Context Quality Evaluator

Evaluates assembled context quality using
context quality metrics.

Sprint:
    S4-011-001 Context Quality Evaluation Foundation

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from typing import Any

from .metrics import (
    calculate_compression_score,
    calculate_coverage_score,
    calculate_diversity_score,
    calculate_overall_score,
    calculate_relevance_score,
    calculate_utility_score,
)

from .models import (
    ContextEvaluationResult,
    ContextQualityScore,
)


class ContextEvaluator:
    """
    Evaluates Context Runtime output quality.

    Responsibilities:

    - calculate quality dimensions
    - aggregate evaluation score
    - return evaluation result

    This evaluator is intentionally stateless.
    """

    def evaluate(
        self,
        *,
        retrieved_items: int,
        selected_items: int,
        relevant_items: int | None = None,
        duplicate_items: int = 0,
        original_tokens: int = 0,
        compressed_tokens: int = 0,
        execution_success: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> ContextEvaluationResult:
        """
        Evaluate context quality.

        Args:

            retrieved_items:
                Number of retrieved context items.

            selected_items:
                Number of selected context items.

            relevant_items:
                Number of relevant selected items.

            duplicate_items:
                Number of duplicated items.

            original_tokens:
                Token count before compression.

            compressed_tokens:
                Token count after compression.

            execution_success:
                Whether downstream execution succeeded.

        Returns:
            ContextEvaluationResult
        """

        relevance = calculate_relevance_score(
            relevant_items
            if relevant_items is not None
            else selected_items,
            selected_items,
        )

        coverage = calculate_coverage_score(
            selected_items,
            retrieved_items,
        )

        diversity = calculate_diversity_score(
            duplicate_items,
            selected_items,
        )

        compression = calculate_compression_score(
            original_tokens,
            compressed_tokens,
        )

        utility = calculate_utility_score(
            success=execution_success,
            context_score=relevance,
        )

        overall = calculate_overall_score(
            relevance_score=relevance,
            coverage_score=coverage,
            diversity_score=diversity,
            compression_score=compression,
            utility_score=utility,
        )

        score = ContextQualityScore(
            relevance_score=relevance,
            coverage_score=coverage,
            diversity_score=diversity,
            compression_score=compression,
            utility_score=utility,
            overall_score=overall,
        )

        return ContextEvaluationResult(
            score=score,
            retrieved_items=retrieved_items,
            selected_items=selected_items,
            metadata=metadata or {},
        )
