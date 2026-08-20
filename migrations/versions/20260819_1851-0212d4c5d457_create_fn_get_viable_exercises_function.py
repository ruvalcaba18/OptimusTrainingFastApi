"""create_fn_get_viable_exercises_function

Revision ID: 0212d4c5d457
Revises: add346a713ab
Create Date: 2026-08-19 18:51:12.989136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0212d4c5d457'
down_revision: Union[str, Sequence[str], None] = 'add346a713ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from pathlib import Path

def upgrade() -> None:
    """Upgrade schema."""
    sql_file = Path(__file__).parent.parent / "sql" / "create_fn_get_viable_exercises.sql"
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()
    op.execute(sa.text(sql))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DROP FUNCTION IF EXISTS fn_get_viable_exercises(INT);"))
