import os
import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from workhub.documents.models import Document
from workhub.audit.service import record_audit_log

# Where uploaded files actually live on disk. Kept next to the project root
# (not inside workhub/) so it's easy to exclude from git and to point a
# backup/volume at in deployment. Created automatically if missing.
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "uploaded_documents")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# SRS Module 7 explicitly lists these four formats as supported.
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "csv"}

# Simple cap so someone can't fill up the disk with one huge upload.
# 20 MB is generous for the formats above and easy to change later.
MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024


def _get_extension(filename: str) -> str:
    """Return the lowercase extension of a filename, without the dot."""
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[-1].lower()


def get_document(document_id: int, db: Session) -> Document:
    """Look up a single document's metadata row by id, or raise 404."""
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        raise HTTPException(detail="Document not found", status_code=status.HTTP_404_NOT_FOUND)
    return document


def service_upload_document(
    file: UploadFile, db: Session, current_user: dict, project_id: int | None = None
):
    """
    'Upload Document' feature from SRS Module 7.

    Validates the file extension against ALLOWED_EXTENSIONS and the file
    size against MAX_FILE_SIZE_BYTES, saves the file to disk under a random
    name (so two people uploading "report.pdf" don't collide), and stores
    a metadata row pointing at it.

    Args:
        file: the incoming multipart file upload.
        db: database session.
        current_user: decoded token dict of whoever is uploading.
        project_id: optional project this document belongs to.

    Returns:
        dict with a success message and the new document_id.
    """
    extension = _get_extension(file.filename or "")
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            detail=f"Unsupported file type '.{extension}'. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    file_bytes = file.file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            detail=f"File is too large. Max allowed size is {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    stored_filename = f"{uuid.uuid4().hex}.{extension}"
    stored_path = os.path.join(UPLOAD_DIRECTORY, stored_filename)
    with open(stored_path, "wb") as out_file:
        out_file.write(file_bytes)

    document = Document(
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_extension=extension,
        project_id=project_id,
        uploaded_by=current_user["user_id"],
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    record_audit_log(
        db,
        "document_uploaded",
        user_id=current_user["user_id"],
        username=current_user.get("username"),
        detail=f"document_id={document.document_id} filename={document.original_filename}",
    )

    return {"message": "Document uploaded successfully", "document_id": document.document_id}


def service_list_documents(db: Session, project_id: int | None = None, skip: int = 0, limit: int = 20):
    """'View Documents' feature from SRS Module 7, with pagination."""
    query = db.query(Document)
    if project_id is not None:
        query = query.filter(Document.project_id == project_id)
    return query.offset(skip).limit(limit).all()


def service_search_documents(db: Session, keyword: str, skip: int = 0, limit: int = 20):
    """'Search Documents' feature from SRS Module 7 / Module 8."""
    like_pattern = f"%{keyword}%"
    return (
        db.query(Document)
        .filter(Document.original_filename.ilike(like_pattern))
        .offset(skip)
        .limit(limit)
        .all()
    )


def service_delete_document(document_id: int, db: Session, current_user: dict):
    """
    'Delete Document' feature from SRS Module 7.

    Only the uploader or an admin can delete a document. Removes both the
    DB row and the file on disk.
    """
    document = get_document(document_id, db)
    if current_user["role"] != "admin" and document.uploaded_by != current_user["user_id"]:
        raise HTTPException(
            detail="Only the uploader or an admin can delete this document",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    stored_path = os.path.join(UPLOAD_DIRECTORY, document.stored_filename)
    if os.path.exists(stored_path):
        os.remove(stored_path)

    db.delete(document)
    db.commit()

    record_audit_log(
        db,
        "document_deleted",
        user_id=current_user["user_id"],
        username=current_user.get("username"),
        detail=f"document_id={document_id}",
    )
    return {"message": "Document deleted successfully"}
