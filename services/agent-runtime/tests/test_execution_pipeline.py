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


class FakeContextRuntime:
    """
    Fake Context Runtime integration.

    Verifies that ExecutionService invokes Context Runtime
    before entering the existing execution pipeline.
    """

    def __init__(self):
        self.calls = []
        self.contexts = []

    def build_context(
        self,
        task,
        agent_context,
    ):
        self.calls.append(task.task_id)
        self.contexts.append(agent_context)

        assembled_context = {
            "text": "assembled context",
            "task_id": task.task_id,
        }

        agent_context.set(
            "assembled_context",
            assembled_context,
        )

        agent_context.set(
            "context_runtime",
            {
                "enabled": True,
                "execution_id": task.task_id,
            },
        )

        return assembled_context


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

    def __init__(self):
        self.contexts = []

    async def invoke(
        self,
        request,
    ):
        self.contexts.append(request.context)

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
    context_runtime = FakeContextRuntime()
    agent_invoker = FakeAgentInvoker()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=agent_invoker,
        trace_recorder=trace_recorder,
        context_runtime=context_runtime,
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
    context_runtime = FakeContextRuntime()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=FailingAgentInvoker(),
        trace_recorder=trace_recorder,
        context_runtime=context_runtime,
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
    context_runtime = FakeContextRuntime()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=FakeAgentInvoker(),
        trace_recorder=trace_recorder,
        context_runtime=context_runtime,
    )

    result = await execution_service.execute(
        task
    )

    assert result.status == TaskStatus.COMPLETED

    assert result.completed_at is not None

    assert len(trace_recorder.traces) == 1


@pytest.mark.anyio
async def test_context_runtime_is_invoked_before_execution():

    task = AgentTask(
        task_id="context-integration-001",
        agent_id="test-agent",
        intent="context_integration_test",
        input={
            "text": "context integration"
        },
        required_capabilities=[
            "echo"
        ],
    )

    task_manager = TaskManager(
        executor=Executor()
    )

    trace_recorder = FakeTraceRecorder()
    context_runtime = FakeContextRuntime()
    agent_invoker = FakeAgentInvoker()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=agent_invoker,
        trace_recorder=trace_recorder,
        context_runtime=context_runtime,
    )

    await execution_service.execute(
        task
    )

    assert context_runtime.calls == [
        "context-integration-001"
    ]

    assert len(context_runtime.contexts) == 1


@pytest.mark.anyio
async def test_context_runtime_enriches_agent_context():

    task = AgentTask(
        task_id="context-integration-002",
        agent_id="test-agent",
        intent="context_enrichment_test",
        input={
            "text": "context enrichment"
        },
        required_capabilities=[
            "echo"
        ],
    )

    task_manager = TaskManager(
        executor=Executor()
    )

    trace_recorder = FakeTraceRecorder()
    context_runtime = FakeContextRuntime()
    agent_invoker = FakeAgentInvoker()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=agent_invoker,
        trace_recorder=trace_recorder,
        context_runtime=context_runtime,
    )

    await execution_service.execute(
        task
    )

    context = context_runtime.contexts[0]

    assert context.get("assembled_context") == {
        "text": "assembled context",
        "task_id": "context-integration-002",
    }

    assert context.get("context_runtime") == {
        "enabled": True,
        "execution_id": "context-integration-002",
    }


@pytest.mark.anyio
async def test_agent_receives_context_enriched_by_context_runtime():

    task = AgentTask(
        task_id="context-integration-003",
        agent_id="test-agent",
        intent="context_propagation_test",
        input={
            "text": "context propagation"
        },
        required_capabilities=[
            "echo"
        ],
    )

    task_manager = TaskManager(
        executor=Executor()
    )

    trace_recorder = FakeTraceRecorder()
    context_runtime = FakeContextRuntime()
    agent_invoker = FakeAgentInvoker()

    execution_service = ExecutionService(
        task_manager=task_manager,
        agent_invoker=agent_invoker,
        trace_recorder=trace_recorder,
        context_runtime=context_runtime,
    )

    await execution_service.execute(
        task
    )

    assert len(context_runtime.contexts) == 1
    assert len(agent_invoker.contexts) == 1

    assert agent_invoker.contexts[0] is context_runtime.contexts[0]

    assert agent_invoker.contexts[0].get(
        "assembled_context"
    ) == {
        "text": "assembled context",
        "task_id": "context-integration-003",
    }

    assert agent_invoker.contexts[0].get(
        "context_runtime"
    ) == {
        "enabled": True,
        "execution_id": "context-integration-003",
    }
