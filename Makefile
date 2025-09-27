# Makefile para Sistema de Gestión de Productos de Panadería

.PHONY: help build up down logs test clean migrate seed

# Comando por defecto
help:
	@echo "Comandos disponibles:"
	@echo "  build     - Construir las imágenes Docker"
	@echo "  up        - Levantar los servicios"
	@echo "  down      - Detener los servicios"
	@echo "  logs      - Ver logs de los servicios"
	@echo "  test      - Ejecutar tests unitarios"
	@echo "  clean     - Limpiar contenedores y volúmenes"
	@echo "  migrate   - Ejecutar migraciones de Alembic"
	@echo "  seed      - Poblar la base de datos con datos de prueba"

# Construir imágenes
build:
	docker-compose build

# Levantar servicios
up:
	docker-compose up -d

# Detener servicios
down:
	docker-compose down

# Ver logs
logs:
	docker-compose logs -f

# Ejecutar tests
test:
	docker-compose exec api pytest -v

# Limpiar contenedores y volúmenes
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Ejecutar migraciones
migrate:
	docker-compose exec api alembic upgrade head

# Poblar base de datos con datos de prueba
seed:
	docker-compose exec api python -c "from app.database import seed_database; seed_database()"

# Comando completo para setup inicial
setup: build up migrate seed
	@echo "Sistema listo! Accede a http://localhost:8000/docs para ver la documentación"
