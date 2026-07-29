import pytest

from app.tasks import (
    TaskLifecycle,
    TaskStatus,
    InvalidTaskTransition,
)


def test_created_to_queued():
    assert (
        TaskLifecycle.transition(
            TaskStatus.CREATED,
            TaskStatus.QUEUED,
        )
        == TaskStatus.QUEUED
    )


def test_queued_to_running():
    assert (
        TaskLifecycle.transition(
            TaskStatus.QUEUED,
            TaskStatus.RUNNING,
        )
        == TaskStatus.RUNNING
    )


def test_running_to_completed():
    assert (
        TaskLifecycle.transition(
            TaskStatus.RUNNING,
            TaskStatus.COMPLETED,
        )
        == TaskStatus.COMPLETED
    )


def test_running_to_failed():
    assert (
        TaskLifecycle.transition(
            TaskStatus.RUNNING,
            TaskStatus.FAILED,
        )
        == TaskStatus.FAILED
    )


def test_invalid_created_to_completed():
    with pytest.raises(InvalidTaskTransition):
        TaskLifecycle.transition(
            TaskStatus.CREATED,
            TaskStatus.COMPLETED,
        )


def test_invalid_completed_to_running():
    with pytest.raises(InvalidTaskTransition):
        TaskLifecycle.transition(
            TaskStatus.COMPLETED,
            TaskStatus.RUNNING,
        )


def test_invalid_failed_to_created():
    with pytest.raises(InvalidTaskTransition):
        TaskLifecycle.transition(
            TaskStatus.FAILED,
            TaskStatus.CREATED,
        )


def test_can_transition_returns_true():
    assert TaskLifecycle.can_transition(
        TaskStatus.CREATED,
        TaskStatus.QUEUED,
    )


def test_can_transition_returns_false():
    assert not TaskLifecycle.can_transition(
        TaskStatus.CREATED,
        TaskStatus.COMPLETED,
    )