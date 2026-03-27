import os
import shutil
import tempfile
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "./upload_docs"

def save_uploaded_file(files: list[UploadFile]) -> list[str]:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_paths = []
    try:
        temp_dir = tempfile.mkdtemp(dir=UPLOAD_DIR)
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            file_paths.append(file_path)
        return file_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
