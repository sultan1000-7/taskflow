from fastapi import APIRouter, status

from taskflow.celery_app import celery_app
from taskflow.schemas.tasks import (
    AddTaskRequest,
    TaskQueuedResponse,
    TaskStatusResponse,
)
from taskflow.tasks.example import add

router = APIRouter()


@router.post(
    "/add",
    response_model=TaskQueuedResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def enqueue_add_task(
    payload: AddTaskRequest,
) -> TaskQueuedResponse:
    task = add.delay(
        payload.x,
        payload.y,
    )

    return TaskQueuedResponse(
        task_id=task.id,
    )


@router.get(
    "/{task_id}",
    response_model=TaskStatusResponse,
)
def get_task_status(
    task_id: str,
) -> TaskStatusResponse:
    task = celery_app.AsyncResult(task_id)

    response = TaskStatusResponse(
        task_id=task_id,
        state=task.state,
    )

    if task.successful():
        response.result = task.result

    elif task.failed():
        response.error = str(task.result)

    return response
