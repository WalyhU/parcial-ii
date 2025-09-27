"""
Tests unitarios para endpoints de productos
"""

import pytest
from decimal import Decimal
from app.models.producto import Producto

class TestProductosEndpoints:
    """Tests para los endpoints de productos"""

    def test_crear_producto_exitoso(self, client, sample_product_data):
        """Test: Crear producto exitosamente"""
        response = client.post("/api/v1/productos/", json=sample_product_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == sample_product_data["nombre"]
        assert data["sku"] == sample_product_data["sku"]
        assert data["categoria"] == sample_product_data["categoria"]
        assert Decimal(str(data["precio_unitario"])) == sample_product_data["precio_unitario"]
        assert data["stock"] == sample_product_data["stock"]
        assert data["disponible"] == sample_product_data["disponible"]
        assert "id" in data
        assert "fecha_registro" in data
        assert "fecha_actualizacion" in data

    def test_crear_producto_sku_duplicado(self, client, sample_product_data):
        """Test: Crear producto con SKU duplicado debe fallar"""
        # Crear primer producto
        client.post("/api/v1/productos/", json=sample_product_data)
        
        # Intentar crear segundo producto con mismo SKU
        response = client.post("/api/v1/productos/", json=sample_product_data)
        
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"]

    def test_crear_producto_datos_invalidos(self, client):
        """Test: Crear producto con datos inválidos debe fallar"""
        invalid_data = {
            "nombre": "",  # Nombre vacío
            "sku": "INVALID",  # SKU formato incorrecto
            "categoria": "Pan",
            "precio_unitario": -1,  # Precio negativo
            "stock": -5,  # Stock negativo
            "disponible": True
        }
        
        response = client.post("/api/v1/productos/", json=invalid_data)
        assert response.status_code == 422

    def test_obtener_producto_por_id_exitoso(self, client, created_product):
        """Test: Obtener producto por ID exitosamente"""
        producto_id = created_product["id"]
        response = client.get(f"/api/v1/productos/{producto_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == producto_id
        assert data["nombre"] == created_product["nombre"]

    def test_obtener_producto_por_id_no_existe(self, client):
        """Test: Obtener producto por ID inexistente debe fallar"""
        response = client.get("/api/v1/productos/999")
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_listar_productos_vacio(self, client, db_session):
        """Test: Listar productos cuando no hay ninguno"""
        # Limpiar base de datos de prueba
        db_session.query(Producto).delete()
        db_session.commit()
        
        response = client.get("/api/v1/productos/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_listar_productos_con_datos(self, client, sample_product_data, sample_product_2_data):
        """Test: Listar productos con datos existentes"""
        # Usar SKUs únicos para evitar conflictos
        sample_product_data["sku"] = "TES-0002"
        sample_product_2_data["sku"] = "TES-0003"
        # Crear productos
        client.post("/api/v1/productos/", json=sample_product_data)
        client.post("/api/v1/productos/", json=sample_product_2_data)
        
        response = client.get("/api/v1/productos/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2

    def test_listar_productos_con_filtros(self, client, sample_product_data, sample_product_2_data):
        """Test: Listar productos con filtros"""
        # Crear productos con categorías específicas
        producto_pan = sample_product_data.copy()
        producto_pan["sku"] = "TES-0004"
        producto_pan["categoria"] = "Pan"
        
        producto_pasteleria = sample_product_2_data.copy()
        producto_pasteleria["sku"] = "TES-0005"
        producto_pasteleria["categoria"] = "Pastelería"
        
        # Crear productos
        client.post("/api/v1/productos/", json=producto_pan)
        client.post("/api/v1/productos/", json=producto_pasteleria)
        
        # Filtrar por categoría Pan
        response = client.get("/api/v1/productos/?categoria=Pan")
        
        assert response.status_code == 200
        data = response.json()
        # Verificar que todos los resultados sean de categoría Pan
        assert all(item["categoria"] == "Pan" for item in data["items"])
        assert data["total"] >= 1

    def test_actualizar_producto_exitoso(self, client, created_product):
        """Test: Actualizar producto exitosamente"""
        producto_id = created_product["id"]
        update_data = {
            "nombre": "Pan Francés Premium",
            "precio_unitario": 1.50,
            "stock": 150
        }
        
        response = client.put(f"/api/v1/productos/{producto_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == update_data["nombre"]
        assert Decimal(str(data["precio_unitario"])) == update_data["precio_unitario"]
        assert data["stock"] == update_data["stock"]

    def test_actualizar_producto_no_existe(self, client):
        """Test: Actualizar producto inexistente debe fallar"""
        update_data = {"nombre": "Producto Inexistente"}
        
        response = client.put("/api/v1/productos/999", json=update_data)
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_actualizar_producto_sku_duplicado(self, client, sample_product_data, sample_product_2_data):
        """Test: Actualizar producto con SKU duplicado debe fallar"""
        # Usar SKUs únicos para evitar conflictos
        sample_product_data["sku"] = "TES-0006"
        sample_product_2_data["sku"] = "TES-0007"
        # Crear dos productos
        response1 = client.post("/api/v1/productos/", json=sample_product_data)
        response2 = client.post("/api/v1/productos/", json=sample_product_2_data)
        
        producto2_id = response2.json()["id"]
        
        # Intentar actualizar segundo producto con SKU del primero
        update_data = {"sku": sample_product_data["sku"]}
        
        response = client.put(f"/api/v1/productos/{producto2_id}", json=update_data)
        
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"]

    def test_eliminar_producto_exitoso(self, client, created_product):
        """Test: Eliminar producto exitosamente"""
        producto_id = created_product["id"]
        
        response = client.delete(f"/api/v1/productos/{producto_id}")
        
        assert response.status_code == 204
        
        # Verificar que el producto fue eliminado
        get_response = client.get(f"/api/v1/productos/{producto_id}")
        assert get_response.status_code == 404

    def test_eliminar_producto_no_existe(self, client):
        """Test: Eliminar producto inexistente debe fallar"""
        response = client.delete("/api/v1/productos/999")
        
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_buscar_productos_por_nombre(self, client, sample_product_data, sample_product_2_data):
        """Test: Buscar productos por nombre"""
        # Crear productos con nombres específicos
        producto_pan = sample_product_data.copy()
        producto_pan["sku"] = "TES-0008"
        producto_pan["nombre"] = "Pan Francés Test"
        
        producto_croissant = sample_product_2_data.copy()
        producto_croissant["sku"] = "TES-0009"
        producto_croissant["nombre"] = "Croissant Test"
        
        # Crear productos
        client.post("/api/v1/productos/", json=producto_pan)
        client.post("/api/v1/productos/", json=producto_croissant)
        
        # Buscar por "Pan"
        response = client.get("/api/v1/productos/buscar/Pan")
        
        assert response.status_code == 200
        data = response.json()
        # Verificar que al menos uno de los resultados contenga "Pan" en el nombre
        assert any("Pan" in item["nombre"] for item in data)

    def test_validacion_categoria_invalida(self, client):
        """Test: Validación de categoría inválida"""
        invalid_data = {
            "nombre": "Producto Test",
            "sku": "TES-0001",
            "categoria": "CategoriaInvalida",
            "precio_unitario": 1.00,
            "stock": 10,
            "disponible": True
        }
        
        response = client.post("/api/v1/productos/", json=invalid_data)
        assert response.status_code == 422

    def test_validacion_precio_cero(self, client):
        """Test: Validación de precio cero"""
        invalid_data = {
            "nombre": "Producto Test",
            "sku": "TES-0001",
            "categoria": "Pan",
            "precio_unitario": 0,
            "stock": 10,
            "disponible": True
        }
        
        response = client.post("/api/v1/productos/", json=invalid_data)
        assert response.status_code == 422

    def test_validacion_stock_negativo(self, client):
        """Test: Validación de stock negativo"""
        invalid_data = {
            "nombre": "Producto Test",
            "sku": "TES-0001",
            "categoria": "Pan",
            "precio_unitario": 1.00,
            "stock": -1,
            "disponible": True
        }
        
        response = client.post("/api/v1/productos/", json=invalid_data)
        assert response.status_code == 422

    def test_endpoint_health_check(self, client):
        """Test: Endpoint de verificación de salud"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "panaderia-api"

    def test_endpoint_root(self, client):
        """Test: Endpoint raíz"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
