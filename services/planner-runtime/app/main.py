from fastapi import FastAPI
from pydantic import BaseModel
from app.llm.ollama_client import OllamaClient

app = FastAPI(
    title="OneMind Planner Runtime",
    version="0.1.0"
)
ollama = OllamaClient()
class PlanRequest(BaseModel):
    prompt: str

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "planner-runtime"
    }
    
@app.post("/plan")
async def plan(request: PlanRequest):
    result = await ollama.generate(request.prompt)

    return {
        "model": ollama.model,
        "response": result,
    }