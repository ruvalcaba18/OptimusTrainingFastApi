"""split_goal_and_method_bridge_tables

Revision ID: 89f6bc157c13
Revises: a69f5758c1f7
Create Date: 2026-06-25 13:24:28.180106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89f6bc157c13'
down_revision: Union[str, Sequence[str], None] = 'a69f5758c1f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
