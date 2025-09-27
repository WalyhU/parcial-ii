"""
Aplicación principal FastAPI para el Sistema de Gestión de Productos de Panadería
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import productos
from app.database import engine
from app.models import producto

# Crear tablas en la base de datos
producto.Base.metadata.create_all(bind=engine)

# Inicializar aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Productos de Panadería",
    description="API REST para gestionar el catálogo de productos de una panadería",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(productos.router, prefix="/api/v1", tags=["productos"])

@app.get("/")
async def root():
    """Endpoint raíz con información básica"""
    return {
        "message": "Sistema de Gestión de Productos de Panadería",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {"status": "healthy", "service": "panaderia-api"}
