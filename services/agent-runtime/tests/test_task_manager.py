import pytest

from app.executor.executor import Executor
from app.manager import TaskManager
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


def create_test_task(
    task_id="task-manager-001",
):
    return AgentTask(
        task_id=task_id,
        agent_id="test-agent",
        intent="task_manager_test",
        input={
            "text": "hello"
        },
        required_capabilities=[
            "echo"
        ],
        status=TaskStatus.CREATED,
    )


def create_task_manager():
    return TaskManager(
        Executor()
    )


def test_create_task():

    manager = create_task_manager()

    task = create_test_task()

    result = manager.create_task(task)

    assert result.task_id == "task-manager-001"
    assert result.status == TaskStatus.CREATED

    assert (
        manager.tasks["task-manager-001"]
        == task
    )


def test_submit_task():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(task)

    result = manager.submit_task(task)

    assert result.status == TaskStatus.QUEUED


@pytest.mark.anyio
async def test_execute_task_success():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(task)

    manager.submit_task(task)

    result = await manager.execute_task(
        task,
        FakeCapabilityManager(),
    )

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

    manager.create_task(task)

    manager.submit_task(task)

    result = await manager.execute_task(
        task,
        FailingCapabilityManager(),
    )

    assert result.status == TaskStatus.FAILED

    assert (
        result.result["error"]
        == "execution_failed"
    )


def test_get_task_status():

    manager = create_task_manager()

    task = create_test_task()

    manager.create_task(task)

    status = manager.get_task_status(
        "task-manager-001"
    )

    assert status == TaskStatus.CREATED


def test_get_task_status_unknown_task():

    manager = create_task_manager()

    with pytest.raises(KeyError):

        manager.get_task_status(
            "unknown-task"
        )