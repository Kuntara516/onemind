import pytest

from app.runtime import ExecutionService
from app.manager import TaskManager
from app.executor import Executor
from app.tasks import AgentTask, TaskStatus

from app.runtime.invocation_result import (
    AgentInvocationResult,
)

from app.runtime.tracing import (
    ExecutionTrace,
)


class FakeAgentInvoker:
    """
    Fake AgentInvoker following Sprint 2 architecture.

    Executor
        |
        v
    AgentInvoker.invoke()
        |
        v
    AgentInvocationResult
    """

    async def invoke(
        self,
        request,
    ):

        return AgentInvocationResult(
            success=True,
            output={
                "echo": request.task.input.get("text")
            },
            metadata={
                "agent_id": request.agent_id,
                "task_id": request.task.task_id,
            },
        )


class FailingAgentInvoker:
    """
    Fake failing AgentInvoker.
    """

    async def invoke(
        self,
        request,
    ):

        return AgentInvocationResult(
            success=False,
            error="capability failed",
            metadata={
                "agent_id": request.agent_id,
                "task_id": request.task.task_id,
            },
        )


class FakeTraceRecorder:
    """
    Fake trace recorder for execution pipeline test.
    """

    def __init__(self):
        self.traces = []


    def record(
        self,
        trace: ExecutionTrace,
    ):
        self.traces.append(
            trace
        )


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

    trace_recorder = FakeTraceRecorder()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=FakeAgentInvoker(),
        trace_recorder=trace_recorder,
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.COMPLETED

    assert result.result == {
        "echo": "hello pipeline"
    }

    assert len(trace_recorder.traces) == 1


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

    trace_recorder = FakeTraceRecorder()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=FailingAgentInvoker(),
        trace_recorder=trace_recorder,
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.FAILED

    assert result.result["error"] == "execution_failed"

    assert len(trace_recorder.traces) == 1


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

    trace_recorder = FakeTraceRecorder()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=FakeAgentInvoker(),
        trace_recorder=trace_recorder,
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.COMPLETED

    assert result.completed_at is not None

    assert len(trace_recorder.traces) == 1