from fastapi.testclient import TestClient

from taskflow.celery_app import celery_app
from taskflow.main import app
from taskflow.tasks.example import add

client = TestClient(app)


def test_add_task_logic() -> None:
    result = add.run(2, 3)

    assert result == 5


def test_enqueue_add_task(monkeypatch) -> None:
    class FakeTask:
        id = "test-task-id"

    def fake_delay(x: int, y: int) -> FakeTask:
        assert x == 2
        assert y == 3

        return FakeTask()

    monkeypatch.setattr(
        add,
        "delay",
        fake_delay,
    )

    response = client.post(
        "/api/v1/tasks/add",
        json={
            "x": 2,
            "y": 3,
        },
    )

    assert response.status_code == 202

    assert response.json() == {
        "task_id": "test-task-id",
        "status": "queued",
    }


def test_get_successful_task(monkeypatch) -> None:
    class FakeAsyncResult:
        state = "SUCCESS"
        result = 5

        @staticmethod
        def successful() -> bool:
            return True

        @staticmethod
        def failed() -> bool:
            return False

    def fake_async_result(task_id: str) -> FakeAsyncResult:
        assert task_id == "test-task-id"

        return FakeAsyncResult()

    monkeypatch.setattr(
        celery_app,
        "AsyncResult",
        fake_async_result,
    )

    response = client.get("/api/v1/tasks/test-task-id")

    assert response.status_code == 200

    assert response.json() == {
        "task_id": "test-task-id",
        "state": "SUCCESS",
        "result": 5,
        "error": None,
    }
