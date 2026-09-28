from io import BytesIO

import pandas as pd
from fastapi.testclient import TestClient

from taskflow.main import app

client = TestClient(app)


def test_import_csv() -> None:
    content = b"name,age\nIvan,25\nAlex,30\n"

    response = client.post(
        "/api/v1/files/import",
        files={
            "file": (
                "users.csv",
                content,
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "users.csv"
    assert data["file_type"] == "csv"
    assert data["rows_count"] == 2
    assert data["columns"] == ["name", "age"]


def test_import_xlsx() -> None:
    buffer = BytesIO()

    dataframe = pd.DataFrame(
        {
            "name": ["Ivan", "Alex"],
            "age": [25, 30],
        }
    )

    dataframe.to_excel(
        buffer,
        index=False,
        engine="openpyxl",
    )

    buffer.seek(0)

    response = client.post(
        "/api/v1/files/import",
        files={
            "file": (
                "users.xlsx",
                buffer.getvalue(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["file_type"] == "xlsx"
    assert data["rows_count"] == 2
    assert data["columns"] == ["name", "age"]


def test_reject_unsupported_file() -> None:
    response = client.post(
        "/api/v1/files/import",
        files={
            "file": (
                "users.txt",
                b"hello",
                "text/plain",
            )
        },
    )

    assert response.status_code == 415
