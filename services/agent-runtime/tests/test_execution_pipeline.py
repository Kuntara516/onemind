import pytest

from app.runtime import ExecutionService
from app.manager import TaskManager
from app.executor import Executor
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
async def test_execution_pipeline_success():

    task = AgentTask(
        task_id="pipeline-task-001",
        agent_id="test-agent",
        intent="echo_pipeline_test",
        input={
            "text": "hello pipeline"
        },
        required_capabilities=[
            "echo"
        ],
    )

    task_manager = TaskManager(
        executor=Executor()
    )

    execution_service = ExecutionService(
        task_manager=task_manager,
        capability_manager=FakeCapabilityManager(),
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.COMPLETED

    assert result.result == {
        "echo": "hello pipeline"
    }


@pytest.mark.anyio
async def test_execution_pipeline_failure():

    task = AgentTask(
        task_id="pipeline-task-002",
        agent_id="test-agent",
        intent="failure_pipeline_test",
        input={},
        required_capabilities=[
            "failing"
        ],
    )

    task_manager = TaskManager(
        executor=Executor()
    )

    execution_service = ExecutionService(
        task_manager=task_manager,
        capability_manager=FailingCapabilityManager(),
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.FAILED

    assert result.result["error"] == "execution_failed"


@pytest.mark.anyio
async def test_execution_pipeline_lifecycle_transition():

    task = AgentTask(
        task_id="pipeline-task-003",
        agent_id="test-agent",
        intent="lifecycle_test",
        input={
            "text": "lifecycle"
        },
        required_capabilities=[
            "echo"
        ],
    )

    task_manager = TaskManager(
        executor=Executor()
    )

    execution_service = ExecutionService(
        task_manager=task_manager,
        capability_manager=FakeCapabilityManager(),
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.COMPLETED

    assert result.completed_at is not None