"""
Rutas FastAPI para la gestión de productos
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.producto import producto_crud
from app.schemas.producto import (
    ProductoCreate, 
    ProductoUpdate, 
    ProductoResponse, 
    ProductoListResponse,
    ErrorResponse
)

# Crear router para productos
router = APIRouter()

@router.post(
    "/productos/",
    response_model=ProductoResponse,
    status_code=201,
    summary="Crear producto",
    description="Crear un nuevo producto en el catálogo",
    responses={
        201: {"description": "Producto creado exitosamente"},
        400: {"model": ErrorResponse, "description": "Datos inválidos o SKU duplicado"},
        422: {"model": ErrorResponse, "description": "Error de validación"}
    }
)
async def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo producto
    
    - **nombre**: Nombre del producto (máximo 150 caracteres)
    - **sku**: Código único del producto (formato XXX-NNNN)
    - **categoria**: Categoría (Pan, Pastelería, Bebidas, Otros)
    - **precio_unitario**: Precio por unidad (mayor a 0)
    - **stock**: Cantidad en inventario (mayor o igual a 0)
    - **disponible**: Indica si está disponible (default: true)
    """
    try:
        return producto_crud.create(db=db, producto=producto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/productos/",
    response_model=ProductoListResponse,
    summary="Listar productos",
    description="Obtener lista de productos con filtros opcionales",
    responses={
        200: {"description": "Lista de productos obtenida exitosamente"}
    }
)
async def listar_productos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    disponible: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de productos con filtros opcionales
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar
    - **categoria**: Filtrar por categoría específica
    - **disponible**: Filtrar por disponibilidad
    """
    productos = producto_crud.get_all(
        db=db, 
        skip=skip, 
        limit=limit,
        categoria=categoria,
        disponible=disponible
    )
    
    total = producto_crud.count_all(
        db=db,
        categoria=categoria,
        disponible=disponible
    )
    
    return ProductoListResponse(
        items=productos,
        total=total,
        page=(skip // limit) + 1,
        size=limit
    )

@router.get(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    summary="Obtener producto por ID",
    description="Obtener un producto específico por su ID",
    responses={
        200: {"description": "Producto encontrado"},
        404: {"model": ErrorResponse, "description": "Producto no encontrado"}
    }
)
async def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un producto por su ID
    
    - **producto_id**: ID único del producto
    """
    producto = producto_crud.get_by_id(db=db, producto_id=producto_id)
    if not producto:
        raise HTTPException(
            status_code=404, 
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto

@router.put(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    summary="Actualizar producto",
    description="Actualizar un producto existente",
    responses={
        200: {"description": "Producto actualizado exitosamente"},
        400: {"model": ErrorResponse, "description": "Datos inválidos o SKU duplicado"},
        404: {"model": ErrorResponse, "description": "Producto no encontrado"},
        422: {"model": ErrorResponse, "description": "Error de validación"}
    }
)
async def actualizar_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un producto existente
    
    - **producto_id**: ID del producto a actualizar
    - **nombre**: Nuevo nombre (opcional)
    - **sku**: Nuevo SKU (opcional, debe ser único)
    - **categoria**: Nueva categoría (opcional)
    - **precio_unitario**: Nuevo precio (opcional, mayor a 0)
    - **stock**: Nuevo stock (opcional, mayor o igual a 0)
    - **disponible**: Nueva disponibilidad (opcional)
    """
    try:
        producto = producto_crud.update(db=db, producto_id=producto_id, producto_update=producto_update)
        if not producto:
            raise HTTPException(
                status_code=404, 
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return producto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/productos/{producto_id}",
    status_code=204,
    summary="Eliminar producto",
    description="Eliminar un producto del catálogo",
    responses={
        204: {"description": "Producto eliminado exitosamente"},
        404: {"model": ErrorResponse, "description": "Producto no encontrado"}
    }
)
async def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un producto del catálogo
    
    - **producto_id**: ID del producto a eliminar
    """
    deleted = producto_crud.delete(db=db, producto_id=producto_id)
    if not deleted:
        raise HTTPException(
            status_code=404, 
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return None

@router.get(
    "/productos/buscar/{nombre}",
    response_model=List[ProductoResponse],
    summary="Buscar productos por nombre",
    description="Buscar productos que contengan el término en el nombre",
    responses={
        200: {"description": "Productos encontrados"}
    }
)
async def buscar_productos(
    nombre: str,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Buscar productos por nombre (búsqueda parcial)
    
    - **nombre**: Término de búsqueda en el nombre del producto
    - **skip**: Número de registros a omitir
    - **limit**: Número máximo de registros a retornar
    """
    productos = producto_crud.search_by_nombre(
        db=db, 
        nombre=nombre, 
        skip=skip, 
        limit=limit
    )
    return productos
