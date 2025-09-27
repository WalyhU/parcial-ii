"""
Operaciones CRUD para la entidad Producto
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

class ProductoCRUD:
    """Clase para operaciones CRUD de productos"""

    def create(self, db: Session, producto: ProductoCreate) -> Producto:
        """
        Crear un nuevo producto
        
        Args:
            db: Sesión de base de datos
            producto: Datos del producto a crear
            
        Returns:
            Producto creado
            
        Raises:
            ValueError: Si el SKU ya existe
        """
        # Verificar que el SKU no exista
        existing_product = db.query(Producto).filter(Producto.sku == producto.sku).first()
        if existing_product:
            raise ValueError(f"El SKU {producto.sku} ya existe")
        
        # Crear el producto
        db_producto = Producto(**producto.model_dump())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto

    def get_by_id(self, db: Session, producto_id: int) -> Optional[Producto]:
        """
        Obtener un producto por ID
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto
            
        Returns:
            Producto encontrado o None
        """
        return db.query(Producto).filter(Producto.id == producto_id).first()

    def get_by_sku(self, db: Session, sku: str) -> Optional[Producto]:
        """
        Obtener un producto por SKU
        
        Args:
            db: Sesión de base de datos
            sku: SKU del producto
            
        Returns:
            Producto encontrado o None
        """
        return db.query(Producto).filter(Producto.sku == sku.upper()).first()

    def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        categoria: Optional[str] = None,
        disponible: Optional[bool] = None
    ) -> List[Producto]:
        """
        Obtener todos los productos con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            categoria: Filtrar por categoría
            disponible: Filtrar por disponibilidad
            
        Returns:
            Lista de productos
        """
        query = db.query(Producto)
        
        # Aplicar filtros
        if categoria:
            query = query.filter(Producto.categoria == categoria)
        if disponible is not None:
            query = query.filter(Producto.disponible == disponible)
        
        return query.offset(skip).limit(limit).all()

    def count_all(
        self, 
        db: Session,
        categoria: Optional[str] = None,
        disponible: Optional[bool] = None
    ) -> int:
        """
        Contar total de productos con filtros opcionales
        
        Args:
            db: Sesión de base de datos
            categoria: Filtrar por categoría
            disponible: Filtrar por disponibilidad
            
        Returns:
            Total de productos
        """
        query = db.query(Producto)
        
        # Aplicar filtros
        if categoria:
            query = query.filter(Producto.categoria == categoria)
        if disponible is not None:
            query = query.filter(Producto.disponible == disponible)
        
        return query.count()

    def update(self, db: Session, producto_id: int, producto_update: ProductoUpdate) -> Optional[Producto]:
        """
        Actualizar un producto
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto a actualizar
            producto_update: Datos a actualizar
            
        Returns:
            Producto actualizado o None si no existe
            
        Raises:
            ValueError: Si el SKU ya existe en otro producto
        """
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            return None
        
        # Verificar SKU único si se está actualizando
        if producto_update.sku and producto_update.sku != db_producto.sku:
            existing_product = db.query(Producto).filter(
                and_(Producto.sku == producto_update.sku, Producto.id != producto_id)
            ).first()
            if existing_product:
                raise ValueError(f"El SKU {producto_update.sku} ya existe")
        
        # Actualizar campos
        update_data = producto_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        
        db.commit()
        db.refresh(db_producto)
        return db_producto

    def delete(self, db: Session, producto_id: int) -> bool:
        """
        Eliminar un producto
        
        Args:
            db: Sesión de base de datos
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó, False si no existe
        """
        db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not db_producto:
            return False
        
        db.delete(db_producto)
        db.commit()
        return True

    def search_by_nombre(self, db: Session, nombre: str, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Buscar productos por nombre (búsqueda parcial)
        
        Args:
            db: Sesión de base de datos
            nombre: Término de búsqueda en el nombre
            skip: Número de registros a omitir
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de productos que coinciden
        """
        return db.query(Producto).filter(
            Producto.nombre.ilike(f"%{nombre}%")
        ).offset(skip).limit(limit).all()

# Instancia global del CRUD
producto_crud = ProductoCRUD()
