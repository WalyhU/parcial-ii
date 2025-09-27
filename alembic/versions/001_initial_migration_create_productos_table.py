"""Initial migration - Create productos table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Crear tabla productos
    op.create_table('productos',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=150), nullable=False),
        sa.Column('sku', sa.String(length=20), nullable=False),
        sa.Column('categoria', sa.String(length=20), nullable=False),
        sa.Column('precio_unitario', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.Column('disponible', sa.Boolean(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('fecha_actualizacion', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sku', name='uq_producto_sku')
    )
    
    # Crear índices
    op.create_index(op.f('ix_productos_id'), 'productos', ['id'], unique=False)
    op.create_index(op.f('ix_productos_nombre'), 'productos', ['nombre'], unique=False)
    op.create_index(op.f('ix_productos_sku'), 'productos', ['sku'], unique=False)


def downgrade() -> None:
    # Eliminar índices
    op.drop_index(op.f('ix_productos_sku'), table_name='productos')
    op.drop_index(op.f('ix_productos_nombre'), table_name='productos')
    op.drop_index(op.f('ix_productos_id'), table_name='productos')
    
    # Eliminar tabla
    op.drop_table('productos')
