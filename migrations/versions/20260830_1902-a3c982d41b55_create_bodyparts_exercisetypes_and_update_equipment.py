"""create_bodyparts_exercisetypes_and_update_equipment

Revision ID: a3c982d41b55
Revises: f2a891b7e401
Create Date: 2026-08-30 19:02:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a3c982d41b55'
down_revision: Union[str, Sequence[str], None] = 'f2a891b7e401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Body Parts table
    op.create_table(
        'body_parts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name_en', sa.String(length=100), nullable=False),
        sa.Column('name_es', sa.String(length=100), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_body_parts_code'), 'body_parts', ['code'], unique=True)
    op.create_index(op.f('ix_body_parts_id'), 'body_parts', ['id'], unique=False)
    op.create_index(op.f('ix_body_parts_name_en'), 'body_parts', ['name_en'], unique=True)

    # 2. Exercise Types table
    op.create_table(
        'exercise_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name_en', sa.String(length=100), nullable=False),
        sa.Column('name_es', sa.String(length=100), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_types_code'), 'exercise_types', ['code'], unique=True)
    op.create_index(op.f('ix_exercise_types_id'), 'exercise_types', ['id'], unique=False)
    op.create_index(op.f('ix_exercise_types_name_en'), 'exercise_types', ['name_en'], unique=True)

    # 3. Update Equipment table with name_es and image_url
    op.add_column('equipment', sa.Column('name_es', sa.String(length=100), nullable=True))
    op.add_column('equipment', sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column('equipment', 'image_url')
    op.drop_column('equipment', 'name_es')
    op.drop_index(op.f('ix_exercise_types_name_en'), table_name='exercise_types')
    op.drop_index(op.f('ix_exercise_types_id'), table_name='exercise_types')
    op.drop_index(op.f('ix_exercise_types_code'), table_name='exercise_types')
    op.drop_table('exercise_types')
    op.drop_index(op.f('ix_body_parts_name_en'), table_name='body_parts')
    op.drop_index(op.f('ix_body_parts_id'), table_name='body_parts')
    op.drop_index(op.f('ix_body_parts_code'), table_name='body_parts')
    op.drop_table('body_parts')
