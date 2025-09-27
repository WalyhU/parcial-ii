"""
Configuración de la base de datos PostgreSQL
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# URL de conexión a la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://panaderia_user:panaderia_pass@localhost:5432/panaderia_db"
)

# Crear motor de base de datos
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Crear sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos declarativos
Base = declarative_base()

def get_db():
    """
    Dependency para obtener sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_database():
    """
    Función para poblar la base de datos con datos de prueba
    """
    from app.models.producto import Producto
    from app.crud.producto import producto_crud
    
    db = SessionLocal()
    try:
        # Verificar si ya existen productos
        existing_products = db.query(Producto).first()
        if existing_products:
            print("Los datos de prueba ya existen en la base de datos")
            return
        
        # Datos de prueba
        productos_prueba = [
            {
                "nombre": "Pan Francés",
                "sku": "PAN-0001",
                "categoria": "Pan",
                "precio_unitario": 1.25,
                "stock": 120,
                "disponible": True
            },
            {
                "nombre": "Croissant",
                "sku": "PAS-0101", 
                "categoria": "Pastelería",
                "precio_unitario": 2.75,
                "stock": 60,
                "disponible": True
            },
            {
                "nombre": "Café Americano",
                "sku": "BEB-0201",
                "categoria": "Bebidas", 
                "precio_unitario": 1.50,
                "stock": 200,
                "disponible": True
            },
            {
                "nombre": "Empanada de Pollo",
                "sku": "EMP-0301",
                "categoria": "Otros",
                "precio_unitario": 3.00,
                "stock": 50,
                "disponible": True
            }
        ]
        
        # Insertar productos de prueba
        for producto_data in productos_prueba:
            producto = Producto(**producto_data)
            db.add(producto)
        
        db.commit()
        print(f"Se insertaron {len(productos_prueba)} productos de prueba")
        
    except Exception as e:
        db.rollback()
        print(f"Error al insertar datos de prueba: {e}")
    finally:
        db.close()
