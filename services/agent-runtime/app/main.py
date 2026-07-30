from fastapi import FastAPI

from app.tasks import AgentTask

from app.registry import registry
from app.agents.demo_agent import DemoAgent

from app.capability_manager import CapabilityManager

from app.runtime import ExecutionService
from app.runtime.invoker import AgentInvoker
from app.runtime.tracing import InMemoryTraceRecorder

from app.executor import Executor
from app.manager import TaskManager


# ---------------------------------------------------------
# Dependency Initialization
# ---------------------------------------------------------

# Register built-in agents
registry.register(
    DemoAgent()
)


# Capability Layer
capability_manager = CapabilityManager()


# Agent Invocation Layer
agent_invoker = AgentInvoker(
    registry,
    capability_manager,
)


# Execution Trace Layer
trace_recorder = InMemoryTraceRecorder()


# Execution Pipeline
executor = Executor()

task_manager = TaskManager(
    executor
)


execution_service = ExecutionService(
    task_manager,
    agent_invoker,
    trace_recorder,
)


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="OneMind Agent Runtime",
    version="0.2.0",
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "agent-runtime",
    }


# ---------------------------------------------------------
# Agent Discovery
# ---------------------------------------------------------

@app.get("/agents")
async def agents():

    return {
        "agents": registry.list_agents(),
    }


# ---------------------------------------------------------
# Agent Execution
# ---------------------------------------------------------

@app.post("/execute")
async def execute(
    task: AgentTask,
):

    result = await execution_service.execute(
        task
    )

    return result

# ---------------------------------------------------------
# Execution Trace Debug
# ---------------------------------------------------------

@app.get("/traces")
async def traces():

    return {
        "traces": [
            trace.to_dict()
            for trace in trace_recorder.list()
        ]
    }