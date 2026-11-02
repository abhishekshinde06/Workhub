"""project tabel was ready

Revision ID: 55036e04827d
Revises: 2b61235845a2
Create Date: 2026-08-27 18:15:21.846978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55036e04827d'
down_revision: Union[str, Sequence[str], None] = '2b61235845a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
