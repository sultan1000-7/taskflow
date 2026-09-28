from fastapi import FastAPI

from taskflow.api.routes.files import router as files_router

app = FastAPI(
    title="TaskFlow",
    version="0.1.0",
)

app.include_router(
    files_router,
    prefix="/api/v1/files",
    tags=["files"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
