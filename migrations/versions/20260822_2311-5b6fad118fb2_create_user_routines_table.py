"""create_user_routines_table

Revision ID: 5b6fad118fb2
Revises: 0212d4c5d457
Create Date: 2026-08-22 23:11:10.361692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b6fad118fb2'
down_revision: Union[str, Sequence[str], None] = '0212d4c5d457'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user_routines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('day', sa.Integer(), nullable=False),
        sa.Column('goal', sa.String(), nullable=False),
        sa.Column('level', sa.String(), nullable=False),
        sa.Column('volume', sa.String(), nullable=False),
        sa.Column('sets', sa.Integer(), nullable=False),
        sa.Column('reps', sa.String(), nullable=False),
        sa.Column('rest', sa.String(), nullable=False),
        sa.Column('method_name', sa.String(), nullable=False),
        sa.Column('exercises', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_routines_id'), 'user_routines', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_routines_id'), table_name='user_routines')
    op.drop_table('user_routines')
