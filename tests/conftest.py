"""
Configuración de pytest para tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.producto import Producto

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override de la dependencia de base de datos para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def setup_database():
    """Configurar base de datos de prueba"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(setup_database):
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

@pytest.fixture
def db_session():
    """Sesión de base de datos para tests"""
    db = TestingSessionLocal()
    try:
        # Limpiar base de datos antes de cada test
        db.query(Producto).delete()
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_product_data():
    """Datos de producto de prueba"""
    return {
        "nombre": "Pan Francés",
        "sku": "PAN-0001",
        "categoria": "Pan",
        "precio_unitario": 1.25,
        "stock": 120,
        "disponible": True
    }

@pytest.fixture
def sample_product_2_data():
    """Segundo producto de prueba"""
    return {
        "nombre": "Croissant",
        "sku": "PAS-0101",
        "categoria": "Pastelería",
        "precio_unitario": 2.75,
        "stock": 60,
        "disponible": True
    }

@pytest.fixture
def created_product(client, sample_product_data):
    """Producto creado para tests"""
    # Usar un SKU único para evitar conflictos con datos de prueba
    sample_product_data["sku"] = "TES-0001"
    sample_product_data["nombre"] = "Producto Test"
    response = client.post("/api/v1/productos/", json=sample_product_data)
    if response.status_code == 201:
        return response.json()
    else:
        # Si falla, crear con datos únicos
        sample_product_data["sku"] = "TES-9999"
        response = client.post("/api/v1/productos/", json=sample_product_data)
        return response.json()
