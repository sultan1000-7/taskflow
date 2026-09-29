from fastapi import FastAPI

from taskflow.api.routes.files import router as files_router
from taskflow.api.routes.tasks import router as tasks_router

app = FastAPI(
    title="TaskFlow",
    version="0.1.0",
)

app.include_router(
    files_router,
    prefix="/api/v1/files",
    tags=["files"],
)

app.include_router(
    tasks_router,
    prefix="/api/v1/tasks",
    tags=["tasks"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
