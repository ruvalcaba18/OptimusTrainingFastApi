"""add_image_url_and_exercise_id_to_exercises

Revision ID: e4d7281f9a12
Revises: a3c982d41b55
Create Date: 2026-08-30 19:10:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e4d7281f9a12'
down_revision: Union[str, Sequence[str], None] = 'a3c982d41b55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('excersices', sa.Column('exercise_id', sa.String(length=100), nullable=True))
    op.add_column('excersices', sa.Column('image_url', sa.String(length=500), nullable=True))
    op.create_index(op.f('ix_excersices_exercise_id'), 'excersices', ['exercise_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_excersices_exercise_id'), table_name='excersices')
    op.drop_column('excersices', 'image_url')
    op.drop_column('excersices', 'exercise_id')
