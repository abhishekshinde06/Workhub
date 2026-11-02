from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from workhub.db_connection import Base


class Document(Base):
    """
    Document table for SRS Module 7.

    The actual file bytes are kept on disk (see documents/service.py ->
    UPLOAD_DIRECTORY) rather than in the database, which is the simplest
    approach for a project this size. This row only stores the metadata
    needed to find, list, search and download that file again.

    - stored_filename: the random/unique name the file was saved under on
      disk (to avoid two uploads with the same original name overwriting
      each other).
    - original_filename: the name the user's file had when they uploaded
      it, shown back to them on download/list.
    - project_id: optional -- a document can be linked to a project, or
      uploaded standalone (nullable).
    """

    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False, unique=True)
    file_extension = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
