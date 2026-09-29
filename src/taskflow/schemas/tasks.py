from typing import Literal

from pydantic import BaseModel


class AddTaskRequest(BaseModel):
    x: int
    y: int


class TaskQueuedResponse(BaseModel):
    task_id: str
    status: Literal["queued"] = "queued"


class TaskStatusResponse(BaseModel):
    task_id: str
    state: str
    result: int | None = None
    error: str | None = None
