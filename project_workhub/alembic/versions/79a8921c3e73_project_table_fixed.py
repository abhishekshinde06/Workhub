"""project table fixed

Revision ID: 79a8921c3e73
Revises: 33b334a79a1d
Create Date: 2026-08-27 18:22:05.391141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79a8921c3e73'
down_revision: Union[str, Sequence[str], None] = '33b334a79a1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
