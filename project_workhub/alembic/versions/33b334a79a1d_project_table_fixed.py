"""project table fixed

Revision ID: 33b334a79a1d
Revises: 55036e04827d
Create Date: 2026-08-27 18:20:32.099806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33b334a79a1d'
down_revision: Union[str, Sequence[str], None] = '55036e04827d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
