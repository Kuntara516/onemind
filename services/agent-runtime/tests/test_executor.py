"""
Executor Runtime Tests.

Validates Sprint 2 Executor execution contract.

Sprint 3 Regression Alignment:
- AgentContext
- ExecutionTrace
- Capability Manager
"""

import pytest

from app.executor.executor import Executor

from app.tasks.models import AgentTask
from app.tasks.status import TaskStatus

from app.agents.context import AgentContext
from app.runtime.tracing.trace import ExecutionTrace


class FakeCapabilityManager:
    """
    Fake capability manager for successful execution.
    """

    async def execute(self, capability, payload):
        return {
            "result": payload
        }


class FailingCapabilityManager:
    """
    Fake capability manager for failure execution.
    """

    async def execute(self, capability, payload):
        raise Exception(
            "capability execution failed"
        )


def create_context():
    """
    Create runtime agent context.
    """

    return AgentContext(
        request_id="test-request-001"
    )


def create_trace(
    task_id: str
):
    """
    Create execution trace.
    """

    return ExecutionTrace(
        request_id="test-request-001",
        task_id=task_id,
    )


@pytest.mark.anyio
async def test_executor_success():

    task = AgentTask(
        task_id="task-001",
        agent_id="test-agent",
        intent="echo_test",
        input={
            "text": "hello"
        },
        required_capabilities=[
            "echo"
        ],
        status=TaskStatus.QUEUED,
    )

    executor = Executor()

    result = await executor.execute(
        task,
        FakeCapabilityManager(),
        create_context(),
        create_trace(
            task.task_id
        ),
    )

    assert result is not None


@pytest.mark.anyio
async def test_executor_failure():

    task = AgentTask(
        task_id="task-002",
        agent_id="test-agent",
        intent="failure_test",
        input={},
        required_capabilities=[
            "failing"
        ],
        status=TaskStatus.QUEUED,
    )

    executor = Executor()

    result = await executor.execute(
        task,
        FailingCapabilityManager(),
        create_context(),
        create_trace(
            task.task_id
        ),
    )

    assert result is not None


@pytest.mark.anyio
async def test_executor_runs_from_queued_state():

    task = AgentTask(
        task_id="task-003",
        agent_id="test-agent",
        intent="queued_execution_test",
        input={
            "text": "hello"
        },
        required_capabilities=[
            "echo"
        ],
        status=TaskStatus.QUEUED,
    )

    executor = Executor()

    result = await executor.execute(
        task,
        FakeCapabilityManager(),
        create_context(),
        create_trace(
            task.task_id
        ),
    )

    assert result is not None