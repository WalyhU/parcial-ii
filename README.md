# Sistema de Gestión de Productos de Panadería

API REST desarrollada con FastAPI para gestionar el catálogo de productos de una panadería.

## Características

- **Framework**: FastAPI
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migraciones**: Alembic
- **Tests**: Pytest
- **Containerización**: Docker & Docker Compose
- **Documentación**: Swagger UI automática

## Estructura del Proyecto

```
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Schemas Pydantic
│   ├── crud/           # Operaciones CRUD
│   ├── routes/         # Endpoints FastAPI
│   ├── database.py     # Configuración de BD
│   └── main.py         # Aplicación principal
├── tests/              # Tests unitarios
├── alembic/           # Migraciones
├── docker-compose.yml # Configuración Docker
├── Dockerfile         # Imagen de la aplicación
├── requirements.txt   # Dependencias Python
└── Makefile          # Comandos útiles
```

## Instalación y Uso

### Opción 1: Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd parcial-ii

# Configurar y levantar servicios
make setup

# Verificar que todo funciona
make test
```

### Opción 2: Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar PostgreSQL
# Crear base de datos: panaderia_db
# Usuario: panaderia_user
# Contraseña: panaderia_pass

# Ejecutar migraciones
alembic upgrade head

# Poblar datos de prueba
python -c "from app.database import seed_database; seed_database()"

# Ejecutar aplicación
uvicorn app.main:app --reload

# Ejecutar tests
pytest -v
```

## Endpoints Disponibles

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/productos/` | Crear producto |
| GET | `/api/v1/productos/` | Listar productos |
| GET | `/api/v1/productos/{id}` | Obtener producto por ID |
| PUT | `/api/v1/productos/{id}` | Actualizar producto |
| DELETE | `/api/v1/productos/{id}` | Eliminar producto |
| GET | `/api/v1/productos/buscar/{nombre}` | Buscar por nombre |

### Otros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información básica |
| GET | `/health` | Estado del servicio |
| GET | `/docs` | Documentación Swagger |
| GET | `/redoc` | Documentación ReDoc |

## Modelo de Datos

### Producto

```json
{
  "id": 1,
  "nombre": "Pan Francés",
  "sku": "PAN-0001",
  "categoria": "Pan",
  "precio_unitario": 1.25,
  "stock": 120,
  "disponible": true,
  "fecha_registro": "2024-01-01T00:00:00Z",
  "fecha_actualizacion": "2024-01-01T00:00:00Z"
}
```

### Categorías Válidas

- `Pan`
- `Pastelería`
- `Bebidas`
- `Otros`

### Validaciones

- **nombre**: Obligatorio, máximo 150 caracteres
- **sku**: Obligatorio, único, formato XXX-NNNN
- **categoria**: Obligatorio, debe ser una categoría válida
- **precio_unitario**: Obligatorio, mayor a 0, 2 decimales
- **stock**: Obligatorio, mayor o igual a 0
- **disponible**: Opcional, default true

## Datos de Prueba

El sistema incluye datos de prueba que se cargan automáticamente:

```json
[
  {
    "nombre": "Pan Francés",
    "sku": "PAN-0001",
    "categoria": "Pan",
    "precio_unitario": 1.25,
    "stock": 120
  },
  {
    "nombre": "Croissant",
    "sku": "PAS-0101",
    "categoria": "Pastelería",
    "precio_unitario": 2.75,
    "stock": 60
  }
]
```

## Comandos Make

```bash
make help          # Ver comandos disponibles
make build         # Construir imágenes Docker
make up            # Levantar servicios
make down          # Detener servicios
make logs          # Ver logs
make test          # Ejecutar tests
make clean         # Limpiar contenedores
make migrate       # Ejecutar migraciones
make seed          # Poblar datos de prueba
make setup         # Setup completo
```

## Testing

```bash
# Ejecutar todos los tests
pytest -v

# Ejecutar tests específicos
pytest tests/test_productos.py::TestProductosEndpoints::test_crear_producto_exitoso

# Ejecutar con cobertura
pytest --cov=app tests/
```

## Documentación

Una vez que la aplicación esté ejecutándose:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Tecnologías Utilizadas

- **FastAPI 0.104.1**: Framework web moderno y rápido
- **PostgreSQL 15**: Base de datos relacional
- **SQLAlchemy 2.0.23**: ORM para Python
- **Alembic 1.12.1**: Herramienta de migraciones
- **Pydantic 2.5.0**: Validación de datos
- **Pytest 7.4.3**: Framework de testing
- **Docker & Docker Compose**: Containerización

## Criterios de Evaluación Cumplidos

✅ **Funcionalidad (35%)**: CRUD completo, validaciones, manejo de errores 400/404
✅ **Arquitectura (25%)**: Separación en models, schemas, crud, routes
✅ **Calidad de Código (20%)**: Código limpio, comentado, bien estructurado
✅ **Tests (10%)**: Tests unitarios completos con Pytest
✅ **Docker y Docs (10%)**: Docker Compose funcional y documentación accesible

## Desarrollo

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## Licencia

Este proyecto es parte del curso de Análisis de Sistemas II de la Universidad Mariano Gálvez de Guatemala.
