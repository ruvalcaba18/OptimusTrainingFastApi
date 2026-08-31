"""create_muscles_tables

Revision ID: f2a891b7e401
Revises: c912d5a06ceb
Create Date: 2026-08-30 18:59:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f2a891b7e401'
down_revision: Union[str, Sequence[str], None] = 'c912d5a06ceb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'muscles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('common_name', sa.String(length=100), nullable=True),
        sa.Column('body_part', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_muscles_code'), 'muscles', ['code'], unique=True)
    op.create_index(op.f('ix_muscles_id'), 'muscles', ['id'], unique=False)
    op.create_index(op.f('ix_muscles_name'), 'muscles', ['name'], unique=True)

    op.create_table(
        'excersice_muscles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('excersice_id', sa.Integer(), nullable=False),
        sa.Column('muscle_id', sa.Integer(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='true'),
        sa.ForeignKeyConstraint(['excersice_id'], ['excersices.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['muscle_id'], ['muscles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_excersice_muscles_id'), 'excersice_muscles', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_excersice_muscles_id'), table_name='excersice_muscles')
    op.drop_table('excersice_muscles')
    op.drop_index(op.f('ix_muscles_name'), table_name='muscles')
    op.drop_index(op.f('ix_muscles_id'), table_name='muscles')
    op.drop_index(op.f('ix_muscles_code'), table_name='muscles')
    op.drop_table('muscles')
