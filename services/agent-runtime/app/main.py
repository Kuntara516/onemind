from fastapi import FastAPI

from app.models import AgentTask
from app.runtime import runtime
from app.registry import registry
from app.agents.demo_agent import DemoAgent
from app.capability_manager import CapabilityManager


# ---------------------------------------------------------
# Agent Registration
# ---------------------------------------------------------
# Register built-in agents when Agent Runtime starts
# ---------------------------------------------------------

registry.register(DemoAgent())
capability_manager = CapabilityManager()


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="OneMind Agent Runtime",
    version="0.1.0"
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "agent-runtime"
    }


# ---------------------------------------------------------
# Agent Discovery
# ---------------------------------------------------------

@app.get("/agents")
async def agents():

    return {
        "agents": registry.list_agents()
    }


# ---------------------------------------------------------
# Agent Execution
# ---------------------------------------------------------

@app.post("/execute")
async def execute(task: AgentTask):

    return await runtime.execute(
        task.agent,
        capability_manager,
        task.task
    )