"""add_exercise_catalog_tables

Revision ID: f7a50c10c5eb
Revises: 7ce7523512ad
Create Date: 2026-06-23 12:40:10.693256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f7a50c10c5eb'
down_revision: Union[str, Sequence[str], None] = '7ce7523512ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conditions_code'), 'conditions', ['code'], unique=True)
    op.create_index(op.f('ix_conditions_id'), 'conditions', ['id'], unique=False)
    op.create_table('excersices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('muscle_group', sa.String(length=100), nullable=False),
    sa.Column('pattern', sa.Enum('DOMINANTE_RODILLA', 'DOMINANTE_CADERA', 'DOMINANTE_CADERA_UNILATERAL', 'UNILATERAL', 'FLEXION_RODILLA', 'EXTENSION_RODILLA', 'FLEXION_PLANTAR', 'EXTENSION_CADERA', 'ABDUCCION', 'ADUCCION', 'ISOMETRICO', 'PLIOMETRIA', 'PLIOMETRICO', 'EMPUJE_HORIZONTAL', 'EMPUJE_INCLINADO', 'EMPUJE_DECLINADO', 'EMPUJE_UNILATERAL', 'EMPUJE_VERTICAL', 'EMPUJE_VERTICAL_EXPLOSIVO', 'EMPUJE_DIAGONAL', 'EMPUJE_DINAMICO', 'TRACCION_HORIZONTAL', 'TRACCION_HORIZONTAL_UNILATERAL', 'TRACCION_VERTICAL', 'TRACCION_PARCIAL', 'ADUCCION_HORIZONTAL', 'ABDUCCION_HORIZONTAL', 'ABDUCCION_HOMBRO', 'EXTENSION_HOMBRO', 'FLEXION_HOMBRO', 'ELEVACION_ESCAPULAR', 'RETRACCION_ESCAPULAR', 'CONTROL_ESCAPULAR', 'ESTABILIDAD_ESCAPULAR', 'EXTENSION_ESPINAL', 'TRANSPORTE_DE_CARGA', 'LOCOMOCION', 'LOCOMOCION_NO_ACCENT', 'ANTI_ROTACION', 'ANTIROTACIONAL', 'ANTIROTACIONAL_METABOLICO', 'ROTACIONAL', 'FLEXION_DE_CODO', 'FLEXION_DE_CODO_NEUTRA', 'FLEXION_DE_CODO_UNILATERAL', 'EXTENSION_DE_CODO', 'ROTACION_EXTERNA_EMPUJE', 'CORE_ANTERIOR', 'CORE_POSTERIOR', 'CORE_LATERAL', 'CORE_AVANZADO', 'MOVILIDAD_CORE', 'ESTABILIZACION', 'AEROBICO', 'ANAEROBICO', 'MIXTO', 'AGILIDAD', 'CORE_METABOLICO', name='excersice_pattern'), nullable=False),
    sa.Column('primary_tool', sa.String(length=100), nullable=False),
    sa.Column('secondary_tool', sa.String(length=100), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('complexity', sa.String(length=50), nullable=False),
    sa.Column('level', sa.String(length=100), nullable=False),
    sa.Column('fatigue', sa.String(length=50), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_excersices_code'), 'excersices', ['code'], unique=True)
    op.create_index(op.f('ix_excersices_id'), 'excersices', ['id'], unique=False)
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goals_code'), 'goals', ['code'], unique=True)
    op.create_index(op.f('ix_goals_id'), 'goals', ['id'], unique=False)
    op.create_table('levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_levels_code'), 'levels', ['code'], unique=True)
    op.create_index(op.f('ix_levels_id'), 'levels', ['id'], unique=False)
    op.create_table('methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('level', sa.String(length=100), nullable=False),
    sa.Column('complexity', sa.String(length=50), nullable=False),
    sa.Column('intensity', sa.String(length=50), nullable=True),
    sa.Column('tempo', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_methods_code'), 'methods', ['code'], unique=True)
    op.create_index(op.f('ix_methods_id'), 'methods', ['id'], unique=False)
    op.create_table('excersice_condition',
    sa.Column('excersice_id', sa.Integer(), nullable=False),
    sa.Column('condition_id', sa.Integer(), nullable=False),
    sa.Column('relationship', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['condition_id'], ['conditions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['excersice_id'], ['excersices.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('excersice_id', 'condition_id')
    )
    op.create_table('excersice_goal',
    sa.Column('excersice_id', sa.Integer(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['excersice_id'], ['excersices.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('excersice_id', 'goal_id')
    )
    op.create_table('method_goal',
    sa.Column('method_id', sa.Integer(), nullable=False),
    sa.Column('goal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['method_id'], ['methods.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('method_id', 'goal_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('method_goal')
    op.drop_table('excersice_goal')
    op.drop_table('excersice_condition')
    op.drop_index(op.f('ix_methods_id'), table_name='methods')
    op.drop_index(op.f('ix_methods_code'), table_name='methods')
    op.drop_table('methods')
    op.drop_index(op.f('ix_levels_id'), table_name='levels')
    op.drop_index(op.f('ix_levels_code'), table_name='levels')
    op.drop_table('levels')
    op.drop_index(op.f('ix_goals_id'), table_name='goals')
    op.drop_index(op.f('ix_goals_code'), table_name='goals')
    op.drop_table('goals')
    op.drop_index(op.f('ix_excersices_id'), table_name='excersices')
    op.drop_index(op.f('ix_excersices_code'), table_name='excersices')
    op.drop_table('excersices')
    op.drop_index(op.f('ix_conditions_id'), table_name='conditions')
    op.drop_index(op.f('ix_conditions_code'), table_name='conditions')
    op.drop_table('conditions')
    # ### end Alembic commands ###
