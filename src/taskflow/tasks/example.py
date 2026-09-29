from taskflow.celery_app import celery_app


@celery_app.task(name="taskflow.add")
def add(x: int, y: int) -> int:
    return x + y
