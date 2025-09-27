"""
Schemas Pydantic para validación de datos de productos
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models.producto import CategoriaProducto

class ProductoBase(BaseModel):
    """Schema base para productos"""
    nombre: str = Field(..., min_length=1, max_length=150, description="Nombre del producto")
    sku: str = Field(..., min_length=3, max_length=20, description="Código único del producto")
    categoria: CategoriaProducto = Field(..., description="Categoría del producto")
    precio_unitario: Decimal = Field(..., gt=0, description="Precio por unidad")
    stock: int = Field(..., ge=0, description="Cantidad en inventario")
    disponible: bool = Field(default=True, description="Indica si el producto está disponible")

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v):
        """Validar formato de SKU"""
        if not v:
            raise ValueError('El SKU no puede estar vacío')
        # Permitir formato como PAN-0001, PAS-0101, etc.
        if len(v.split('-')) != 2:
            raise ValueError('El SKU debe tener formato XXX-NNNN (ej: PAN-0001)')
        return v.upper()

    @field_validator('precio_unitario')
    @classmethod
    def validate_precio(cls, v):
        """Validar precio unitario"""
        if v <= 0:
            raise ValueError('El precio unitario debe ser mayor a 0')
        # Verificar que tenga máximo 2 decimales
        if v.as_tuple().exponent < -2:
            raise ValueError('El precio unitario no puede tener más de 2 decimales')
        return v

    @field_validator('stock')
    @classmethod
    def validate_stock(cls, v):
        """Validar stock"""
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

class ProductoCreate(ProductoBase):
    """Schema para crear un producto"""
    pass

class ProductoUpdate(BaseModel):
    """Schema para actualizar un producto (todos los campos opcionales)"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    sku: Optional[str] = Field(None, min_length=3, max_length=20)
    categoria: Optional[CategoriaProducto] = None
    precio_unitario: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v):
        """Validar formato de SKU si se proporciona"""
        if v is not None:
            if not v:
                raise ValueError('El SKU no puede estar vacío')
            if len(v.split('-')) != 2:
                raise ValueError('El SKU debe tener formato XXX-NNNN (ej: PAN-0001)')
            return v.upper()
        return v

    @field_validator('precio_unitario')
    @classmethod
    def validate_precio(cls, v):
        """Validar precio unitario si se proporciona"""
        if v is not None:
            if v <= 0:
                raise ValueError('El precio unitario debe ser mayor a 0')
            # Verificar que tenga máximo 2 decimales
            if v.as_tuple().exponent < -2:
                raise ValueError('El precio unitario no puede tener más de 2 decimales')
        return v

    @field_validator('stock')
    @classmethod
    def validate_stock(cls, v):
        """Validar stock si se proporciona"""
        if v is not None and v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v

class ProductoResponse(ProductoBase):
    """Schema para respuesta de producto"""
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    model_config = {"from_attributes": True}

class ProductoListResponse(BaseModel):
    """Schema para respuesta de lista de productos"""
    items: list[ProductoResponse]
    total: int
    page: int = 1
    size: int = 100

class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    detail: str
    error_code: Optional[str] = None
