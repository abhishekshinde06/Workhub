"""
Recreate the audit_log table from the current model in workhub/audit/models.py.

Run this ONCE, from the project root (same place you run `uvicorn main:app`),
after pulling in the updated workhub/audit/models.py that has:
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)

What it does:
1. Drops the existing audit_log table (this clears old audit log rows --
   nothing else in your database is touched: users, projects, tasks,
   comments, documents all stay exactly as they are).
2. Recreates audit_log using the model definition, which now includes
   ON DELETE CASCADE on the user_id foreign key.

Usage:
    python recreate_audit_log_table.py
"""

from workhub.db_connection import engine
from workhub.audit.models import AuditLog

if __name__ == "__main__":
    print("Dropping existing audit_log table (if it exists)...")
    AuditLog.__table__.drop(bind=engine, checkfirst=True)

    print("Recreating audit_log table from the model (with ON DELETE CASCADE)...")
    AuditLog.__table__.create(bind=engine, checkfirst=True)

    print("Done. audit_log.user_id now cascades on user deletion.")
