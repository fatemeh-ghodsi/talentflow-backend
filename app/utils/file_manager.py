import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.logger import logger 
from app.exceptions import InvalidFileError

# CONFIG
UPLOAD_DIR = Path("uploads")
MAX_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def save_file(file: UploadFile) -> str:
    if not UPLOAD_DIR.exists():
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    if not file.filename:
        raise InvalidFileError("Invalid filename")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise InvalidFileError(f"Extension {ext} not allowed")
    
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0) 
    
    if size > MAX_SIZE:
        raise InvalidFileError("File size is too large")
    
    file_name = f"{uuid.uuid4()}{ext}"
    file_path = UPLOAD_DIR / file_name 

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        logger.exception("Error saving file")
        raise
    finally:
        file.file.close()
        
    return str(file_path)

def delete_file(path: str | None):
    if not path:
        return
        
    file_path = Path(path)
    if file_path.exists():
        try:
            file_path.unlink() 
        except Exception as e:
            logger.warning(f"Failed to delete file {path}: {e}")
