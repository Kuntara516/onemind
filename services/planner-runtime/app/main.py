from fastapi import FastAPI

app = FastAPI(
    title="OneMind Planner Runtime",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "planner-runtime"
    }