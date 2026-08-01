"""
Task Manager Runtime Tests.

Validates TaskManager execution lifecycle contract.

Sprint 3 Regression Alignment:
- AgentContext
- ExecutionTrace
- Executor Contract
- Task Lifecycle Management
"""

import pytest

from app.manager.task_manager import TaskManager
from app.executor.executor import Executor

from app.tasks.models import AgentTask
from app.tasks.status import TaskStatus

from app.agents.context import AgentContext
from app.runtime.tracing.trace import ExecutionTrace


class FakeCapabilityManager:
    """
    Fake agent invoker substitute for successful execution.

    Current architecture:

    TaskManager
        |
        Executor
        |
        AgentInvoker

    The object passed here only satisfies
    Executor invocation contract for tests.
    """

    async def invoke(self, request):
        from app.runtime.invocation_result import (
            AgentInvocationResult,
        )

        return AgentInvocationResult(
            success=True,
            output={
                "echo": request.task.input.get(
                    "text"
                )
            },
        )


class FailingCapabilityManager:
    """
    Fake agent invoker substitute for failure execution.
    """

    async def invoke(self, request):
        from app.runtime.invocation_result import (
            AgentInvocationResult,
        )

        return AgentInvocationResult(
            success=False,
            error="capability execution failed",
        )


def create_task_manager():
    """
    Create TaskManager instance.
    """

    return TaskManager(
        executor=Executor()
    )


def create_context():
    """
    Create runtime execution context.
    """

    return AgentContext(
        request_id="test-request-001"
    )


def create_trace(task_id: str):
    """
    Create execution trace.
    """

    return ExecutionTrace(
        request_id="test-request-001",
        task_id=task_id,
    )


def create_test_task():

    return AgentTask(
        task_id="task-manager-001",
        agent_id="test-agent",
        intent="manager_test",
        input={
            "text": "hello"
        },
        required_capabilities=[
            "echo"
        ],
        status=TaskStatus.CREATED,
    )


def test_create_task_registers_task():

    manager = create_task_manager()

    task = create_test_task()

    result = manager.create_task(
        task
    )

    assert result == task

    assert task.task_id in manager.tasks

    assert manager.tasks[
        task.task_id
    ] == task


def test_submit_task_moves_to_queued():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(
        task
    )

    result = manager.submit_task(
        task
    )

    assert result.status == TaskStatus.QUEUED

    assert manager.tasks[
        task.task_id
    ].status == TaskStatus.QUEUED


def test_get_task_status():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(
        task
    )

    status = manager.get_task_status(
        task.task_id
    )

    assert status == TaskStatus.CREATED


@pytest.mark.anyio
async def test_execute_task_success():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(
        task
    )

    manager.submit_task(
        task
    )

    result = await manager.execute_task(
        task,
        FakeCapabilityManager(),
        create_context(),
        create_trace(
            task.task_id
        ),
    )

    assert result is not None

    assert result.status == TaskStatus.COMPLETED

    assert result.result == {
        "echo": "hello"
    }


@pytest.mark.anyio
async def test_execute_task_failure():

    manager = create_task_manager()

    task = AgentTask(
        task_id="task-manager-failure",
        agent_id="test-agent",
        intent="failure_test",
        input={},
        required_capabilities=[
            "failing"
        ],
        status=TaskStatus.CREATED,
    )

    manager.create_task(
        task
    )

    manager.submit_task(
        task
    )

    result = await manager.execute_task(
        task,
        FailingCapabilityManager(),
        create_context(),
        create_trace(
            task.task_id
        ),
    )

    assert result is not None

    assert result.status == TaskStatus.FAILED


@pytest.mark.anyio
async def test_task_lifecycle_after_execution():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(
        task
    )

    manager.submit_task(
        task
    )

    await manager.execute_task(
        task,
        FakeCapabilityManager(),
        create_context(),
        create_trace(
            task.task_id
        ),
    )

    assert task.status in [
        TaskStatus.COMPLETED,
        TaskStatus.FAILED,
    ]