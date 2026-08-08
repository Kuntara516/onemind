"""
Context Runtime Evaluation Integration

Integration adapter between Context Runtime
outputs, Context Quality Evaluation,
and Runtime Feedback.

Sprint:
    S4-011-002 Context Evaluation Integration
    S4-011-003 Context Evaluation & Runtime Feedback

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

from .feedback import (
    ContextRuntimeFeedback,
)

from .feedback_models import (
    ContextRuntimeFeedbackResult,
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
    - generate runtime feedback from evaluation results
    - isolate runtime from evaluator and feedback implementations
    """

    def __init__(
        self,
        evaluator: ContextEvaluator | None = None,
        feedback: ContextRuntimeFeedback | None = None,
    ) -> None:

        self.evaluator = (
            evaluator
            or ContextEvaluator()
        )

        self.feedback = (
            feedback
            or ContextRuntimeFeedback()
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

        Existing S4-011-002 contract is preserved.
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

    def generate_feedback(
        self,
        evaluation: ContextEvaluationResult,
    ) -> ContextRuntimeFeedbackResult:
        """
        Generate runtime feedback from an evaluation result.

        This is intentionally a separate downstream operation and does not
        alter the existing evaluation contract.
        """

        return self.feedback.generate(
            evaluation
        )
