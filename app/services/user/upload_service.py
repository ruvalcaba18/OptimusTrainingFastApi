import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

BASE_DIR = Path(__file__).resolve().parent.parent 
UPLOAD_DIR = BASE_DIR / "uploads" / "profile_pictures"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def _validate_image(file: UploadFile) -> str:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato no permitido. Usa: {', '.join(ALLOWED_EXTENSIONS)}",
        )
    return ext


async def save_profile_picture(user_id: int, file: UploadFile) -> str:
    ext = _validate_image(file)

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"La imagen no puede superar {MAX_FILE_SIZE_MB} MB.",
        )

    filename = f"{user_id}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = UPLOAD_DIR / filename

    for old in UPLOAD_DIR.glob(f"{user_id}_*"):
        old.unlink(missing_ok=True)

    with open(file_path, "wb") as f:
        f.write(content)

    return f"/uploads/profile_pictures/{filename}"


def delete_profile_picture(user_id: int) -> None:
    for old in UPLOAD_DIR.glob(f"{user_id}_*"):
        old.unlink(missing_ok=True)
