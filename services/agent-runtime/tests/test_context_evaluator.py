"""
Context Runtime Context Evaluation Tests

Sprint:
    S4-011-001 Context Quality Evaluation Foundation

Coverage:

- ContextEvaluator execution
- quality score calculation
- metadata propagation
"""

from app.context_runtime.evaluation import (
    ContextEvaluator,
)


def test_context_evaluator_basic_evaluation():

    evaluator = ContextEvaluator()

    result = evaluator.evaluate(
        retrieved_items=10,
        selected_items=5,
        relevant_items=4,
        duplicate_items=1,
        original_tokens=1000,
        compressed_tokens=400,
        execution_success=True,
    )

    assert result.retrieved_items == 10
    assert result.selected_items == 5

    assert (
        result.score.relevance_score
        == 0.8
    )

    assert (
        result.score.coverage_score
        == 0.5
    )

    assert (
        result.score.diversity_score
        == 0.8
    )

    assert (
        result.score.compression_score
        == 0.6
    )

    assert (
        result.score.utility_score
        == 0.8
    )

    assert (
        0 <= result.score.overall_score <= 1
    )


def test_context_evaluator_failed_execution():

    evaluator = ContextEvaluator()

    result = evaluator.evaluate(
        retrieved_items=5,
        selected_items=2,
        execution_success=False,
    )

    assert (
        result.score.utility_score
        == 0
    )


def test_context_evaluator_metadata():

    evaluator = ContextEvaluator()

    result = evaluator.evaluate(
        retrieved_items=3,
        selected_items=2,
        metadata={
            "task_id": "task-001",
        },
    )

    assert (
        result.metadata["task_id"]
        == "task-001"
    )
