import json
from pathlib import Path
from typing import BinaryIO

import pandas as pd


class UnsupportedFileTypeError(Exception):
    pass


def import_file(
    file: BinaryIO,
    filename: str,
) -> tuple[pd.DataFrame, str]:
    extension = Path(filename).suffix.lower()

    if extension == ".csv":
        dataframe = _read_csv(file)
        file_type = "csv"

    elif extension == ".xlsx":
        file.seek(0)
        dataframe = pd.read_excel(
            file,
            engine="openpyxl",
        )
        file_type = "xlsx"

    else:
        raise UnsupportedFileTypeError("Only CSV and XLSX files are supported.")

    dataframe.columns = [str(column).strip() for column in dataframe.columns]

    return dataframe, file_type


def make_preview(
    dataframe: pd.DataFrame,
    limit: int = 5,
) -> list[dict]:
    preview_json = dataframe.head(limit).to_json(
        orient="records",
        date_format="iso",
    )

    return json.loads(preview_json)


def _read_csv(file: BinaryIO) -> pd.DataFrame:
    encodings = (
        "utf-8-sig",
        "utf-8",
        "cp1251",
    )

    last_error: UnicodeDecodeError | None = None

    for encoding in encodings:
        try:
            file.seek(0)

            return pd.read_csv(
                file,
                encoding=encoding,
                sep=None,
                engine="python",
            )

        except UnicodeDecodeError as exc:
            last_error = exc

    if last_error is not None:
        raise last_error

    raise RuntimeError("Unable to read CSV file.")
