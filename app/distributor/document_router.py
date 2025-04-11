# app/distributor/document_router.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database.session import get_db
from jwt_auth.dependencies import verify_token
import os, shutil

router = APIRouter(prefix="/distributor/documents", tags=["Distributor Documents"])

@router.post("/upload/{investor_id}")
def upload_document(
    investor_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    folder = f"uploads/investors/{investor_id}"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "✅ Document uploaded", "path": file_path}

@router.get("/list/{investor_id}")
def list_documents(investor_id: int):
    folder = f"uploads/investors/{investor_id}"
    if not os.path.exists(folder):
        return []
    return os.listdir(folder)
