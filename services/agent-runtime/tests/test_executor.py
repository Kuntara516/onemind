import pytest

from app.executor.executor import Executor
from app.tasks import AgentTask, TaskStatus


class FakeCapability:
    async def execute(self, **kwargs):
        return {
            "echo": kwargs.get("text")
        }


class FakeCapabilityManager:
    def resolve(self, required_capabilities):
        return FakeCapability()


class FailingCapability:
    async def execute(self, **kwargs):
        raise Exception("capability failed")


class FailingCapabilityManager:
    def resolve(self, required_capabilities):
        return FailingCapability()


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
    )

    assert result.status == TaskStatus.COMPLETED
    assert result.result == {
        "echo": "hello"
    }


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
    )

    assert result.status == TaskStatus.FAILED
    assert result.result["error"] == "execution_failed"


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
    )

    assert result.status == TaskStatus.COMPLETED
    assert result.result == {
        "echo": "hello"
    }