"""
Context Runtime Evaluation Integration

Integration adapter between Context Runtime
outputs and Context Quality Evaluation.

Sprint:
    S4-011-002 Context Evaluation Integration

Author:
    OneMind Platform

License:
    MIT
"""

from __future__ import annotations

from typing import Any

from app.context_runtime.models import (
    SelectedContext,
)

from .evaluator import (
    ContextEvaluator,
)

from .models import (
    ContextEvaluationResult,
)


class ContextEvaluationIntegration:
    """
    Evaluation integration adapter.

    Responsibilities:

    - evaluate selected context
    - attach evaluation metadata
    - isolate runtime from evaluator implementation
    """

    def __init__(
        self,
        evaluator: ContextEvaluator | None = None,
    ) -> None:

        self.evaluator = (
            evaluator
            or ContextEvaluator()
        )

    def evaluate_context(
        self,
        context: SelectedContext,
        *,
        execution_success: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> ContextEvaluationResult:
        """
        Evaluate selected context quality.
        """

        result = self.evaluator.evaluate(
            retrieved_items=len(
                context.items
            ),
            selected_items=len(
                context.items
            ),
            original_tokens=context.total_tokens,
            compressed_tokens=context.total_tokens,
            execution_success=execution_success,
            metadata=metadata or {},
        )

        context.metadata[
            "evaluation"
        ] = result.model_dump(
            mode="json"
        )

        return result
