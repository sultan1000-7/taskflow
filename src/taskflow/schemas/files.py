from typing import Any, Literal

from pydantic import BaseModel


class FileImportResult(BaseModel):
    filename: str
    file_type: Literal["csv", "xlsx"]
    rows_count: int
    columns: list[str]
    preview: list[dict[str, Any]]
