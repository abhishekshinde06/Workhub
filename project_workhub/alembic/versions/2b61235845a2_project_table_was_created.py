"""project table was created

Revision ID: 2b61235845a2
Revises: dd0ed7a88e2f
Create Date: 2026-08-27 17:33:43.311522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b61235845a2'
down_revision: Union[str, Sequence[str], None] = 'dd0ed7a88e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
