from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import BinaryIO

from fastapi import HTTPException, UploadFile

from app.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".md"}


def validate_file_extension(filename: str) -> bool:
    """Validate file extension."""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def validate_file_size(size: int) -> bool:
    """Validate file size."""
    return size <= settings.MAX_UPLOAD_SIZE


async def save_upload_file(
    upload_file: UploadFile,
    destination: str | None = None,
) -> str:
    """Save uploaded file to disk."""
    if not validate_file_extension(upload_file.filename or ""):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    if destination:
        file_path = upload_dir / destination
    else:
        file_path = upload_dir / (upload_file.filename or "unnamed")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return str(file_path)


def delete_file(file_path: str) -> bool:
    """Delete file from disk."""
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False
