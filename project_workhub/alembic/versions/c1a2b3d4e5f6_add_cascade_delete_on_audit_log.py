"""add cascade delete on audit_log.user_id

Revision ID: c1a2b3d4e5f6
Revises: fe91e6c6e7b2
Create Date: 2026-09-18

Written by hand rather than via `alembic revision --autogenerate`, because
Alembic's autogenerate does not reliably detect a change to just the
ON DELETE rule of an existing foreign key -- it only detects new/removed
columns, tables and constraints, not this kind of attribute-only change.
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'fe91e6c6e7b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing plain foreign key and recreate it with
    # ON DELETE CASCADE, so deleting a user automatically deletes their
    # audit_log rows too.
    op.drop_constraint('audit_log_user_id_fkey', 'audit_log', type_='foreignkey')
    op.create_foreign_key(
        'audit_log_user_id_fkey',
        source_table='audit_log',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['user_id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    # Revert to a plain foreign key with no cascade behaviour.
    op.drop_constraint('audit_log_user_id_fkey', 'audit_log', type_='foreignkey')
    op.create_foreign_key(
        'audit_log_user_id_fkey',
        source_table='audit_log',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['user_id'],
    )
