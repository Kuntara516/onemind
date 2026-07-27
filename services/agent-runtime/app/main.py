from fastapi import FastAPI

from app.models import AgentTask
from app.runtime import runtime
from app.registry import registry


app = FastAPI(
    title="OneMind Agent Runtime",
    version="0.1.0"
)


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "agent-runtime"
    }


@app.get("/agents")
async def agents():

    return {
        "agents": registry.list_agents()
    }


@app.post("/execute")
async def execute(task: AgentTask):

    return await runtime.execute(
        task.agent,
        task.task
    )