import os
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.documents import service

router = APIRouter(tags=["Documents"])


@router.post("/document")
def upload_document(
    file: UploadFile = File(...),
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Upload Document' feature from SRS Module 7 (pdf, docx, txt, csv)."""
    return service.service_upload_document(file, db, current_user, project_id)


@router.get("/document/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Download Document' feature from SRS Module 7."""
    document = service.get_document(document_id, db)
    file_path = os.path.join(service.UPLOAD_DIRECTORY, document.stored_filename)
    return FileResponse(path=file_path, filename=document.original_filename)


@router.get("/documents")
def list_documents(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'View Documents' feature from SRS Module 7."""
    return service.service_list_documents(db, project_id, skip, limit)


@router.get("/documents/search")
def search_documents(
    keyword: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Search Documents' feature from SRS Module 7."""
    return service.service_search_documents(db, keyword, skip, limit)


@router.delete("/document/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
):
    """'Delete Document' feature from SRS Module 7."""
    return service.service_delete_document(document_id, db, current_user)
