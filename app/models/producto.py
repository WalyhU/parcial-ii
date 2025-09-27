"""
Modelo SQLAlchemy para la entidad Producto
"""

from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum

class CategoriaProducto(str, Enum):
    """Enum para las categorías de productos"""
    PAN = "Pan"
    PASTELERIA = "Pastelería"
    BEBIDAS = "Bebidas"
    OTROS = "Otros"

class Producto(Base):
    """
    Modelo de la tabla productos
    
    Campos:
    - id: Identificador único autoincremental
    - nombre: Nombre del producto (máximo 150 caracteres)
    - sku: Código único del producto (ej. PAN-0001)
    - categoria: Categoría del producto (Pan, Pastelería, Bebidas, Otros)
    - precio_unitario: Precio por unidad (mayor a 0, 2 decimales)
    - stock: Cantidad en inventario (mayor o igual a 0)
    - disponible: Indica si el producto está disponible (default: True)
    - fecha_registro: Fecha de creación del registro
    - fecha_actualizacion: Fecha de última actualización
    """
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, index=True)
    sku = Column(String(20), unique=True, nullable=False, index=True)
    categoria = Column(String(20), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    disponible = Column(Boolean, nullable=False, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Constraint único para SKU
    __table_args__ = (
        UniqueConstraint('sku', name='uq_producto_sku'),
    )

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', sku='{self.sku}')>"
