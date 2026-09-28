from fastapi import APIRouter, File, HTTPException, UploadFile, status

from taskflow.schemas.files import FileImportResult
from taskflow.services.file_importer import (
    UnsupportedFileTypeError,
    import_file,
    make_preview,
)

router = APIRouter()


@router.post(
    "/import",
    response_model=FileImportResult,
)
def import_uploaded_file(
    file: UploadFile = File(...),
) -> FileImportResult:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is missing.",
        )

    try:
        dataframe, file_type = import_file(
            file=file.file,
            filename=file.filename,
        )

    except UnsupportedFileTypeError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read file.",
        ) from exc

    return FileImportResult(
        filename=file.filename,
        file_type=file_type,
        rows_count=len(dataframe),
        columns=list(dataframe.columns),
        preview=make_preview(dataframe),
    )
