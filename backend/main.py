"""DocsMind backend — FastAPI entry point."""
from fastapi import FastAPI

app = FastAPI(title="DocsMind", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe — confirms the API process is up."""
    return {"status": "ok"}