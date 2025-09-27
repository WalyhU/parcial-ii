#!/usr/bin/env python3
"""
Script de demostración para la API de Gestión de Productos de Panadería
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_response(response: requests.Response, title: str = ""):
    """Imprimir respuesta de la API de forma legible"""
    print(f"\n{'='*50}")
    if title:
        print(f"🔍 {title}")
    print(f"Status: {response.status_code}")
    
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print('='*50)

def demo_api():
    """Demostración completa de la API"""
    
    print("🚀 DEMO: Sistema de Gestión de Productos de Panadería")
    print("=" * 60)
    
    # 1. Verificar salud del servicio
    print("\n1️⃣ Verificando salud del servicio...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check")
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API. Asegúrate de que esté ejecutándose en http://localhost:8000")
        return
    
    # 2. Obtener información básica
    print("\n2️⃣ Información básica de la API...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Información Básica")
    
    # 3. Listar productos (inicialmente vacío)
    print("\n3️⃣ Listando productos (inicialmente vacío)...")
    response = requests.get(f"{BASE_URL}/api/v1/productos/")
    print_response(response, "Lista de Productos")
    
    # 4. Crear primer producto
    print("\n4️⃣ Creando primer producto...")
    producto1 = {
        "nombre": "Pan Francés",
        "sku": "PAN-0001",
        "categoria": "Pan",
        "precio_unitario": 1.25,
        "stock": 120,
        "disponible": True
    }
    response = requests.post(f"{BASE_URL}/api/v1/productos/", json=producto1)
    print_response(response, "Producto Creado")
    
    if response.status_code == 201:
        producto1_data = response.json()
        producto1_id = producto1_data["id"]
        
        # 5. Crear segundo producto
        print("\n5️⃣ Creando segundo producto...")
        producto2 = {
            "nombre": "Croissant",
            "sku": "PAS-0101",
            "categoria": "Pastelería",
            "precio_unitario": 2.75,
            "stock": 60,
            "disponible": True
        }
        response = requests.post(f"{BASE_URL}/api/v1/productos/", json=producto2)
        print_response(response, "Segundo Producto Creado")
        
        # 6. Listar todos los productos
        print("\n6️⃣ Listando todos los productos...")
        response = requests.get(f"{BASE_URL}/api/v1/productos/")
        print_response(response, "Lista Completa de Productos")
        
        # 7. Obtener producto por ID
        print(f"\n7️⃣ Obteniendo producto por ID ({producto1_id})...")
        response = requests.get(f"{BASE_URL}/api/v1/productos/{producto1_id}")
        print_response(response, "Producto por ID")
        
        # 8. Actualizar producto
        print(f"\n8️⃣ Actualizando producto {producto1_id}...")
        update_data = {
            "nombre": "Pan Francés Premium",
            "precio_unitario": 1.50,
            "stock": 150
        }
        response = requests.put(f"{BASE_URL}/api/v1/productos/{producto1_id}", json=update_data)
        print_response(response, "Producto Actualizado")
        
        # 9. Buscar productos por nombre
        print("\n9️⃣ Buscando productos por nombre 'Pan'...")
        response = requests.get(f"{BASE_URL}/api/v1/productos/buscar/Pan")
        print_response(response, "Búsqueda por Nombre")
        
        # 10. Filtrar por categoría
        print("\n🔟 Filtrando productos por categoría 'Pastelería'...")
        response = requests.get(f"{BASE_URL}/api/v1/productos/?categoria=Pastelería")
        print_response(response, "Filtro por Categoría")
        
        # 11. Probar validaciones (SKU duplicado)
        print("\n1️⃣1️⃣ Probando validación de SKU duplicado...")
        producto_duplicado = {
            "nombre": "Pan Duplicado",
            "sku": "PAN-0001",  # SKU duplicado
            "categoria": "Pan",
            "precio_unitario": 1.00,
            "stock": 50,
            "disponible": True
        }
        response = requests.post(f"{BASE_URL}/api/v1/productos/", json=producto_duplicado)
        print_response(response, "Error: SKU Duplicado")
        
        # 12. Probar validaciones (datos inválidos)
        print("\n1️⃣2️⃣ Probando validación de datos inválidos...")
        producto_invalido = {
            "nombre": "",  # Nombre vacío
            "sku": "INVALID",  # SKU formato incorrecto
            "categoria": "Pan",
            "precio_unitario": -1,  # Precio negativo
            "stock": -5,  # Stock negativo
            "disponible": True
        }
        response = requests.post(f"{BASE_URL}/api/v1/productos/", json=producto_invalido)
        print_response(response, "Error: Datos Inválidos")
        
        # 13. Eliminar producto
        print(f"\n1️⃣3️⃣ Eliminando producto {producto1_id}...")
        response = requests.delete(f"{BASE_URL}/api/v1/productos/{producto1_id}")
        print(f"Status: {response.status_code} (204 = Eliminado exitosamente)")
        
        # 14. Verificar que fue eliminado
        print(f"\n1️⃣4️⃣ Verificando que el producto {producto1_id} fue eliminado...")
        response = requests.get(f"{BASE_URL}/api/v1/productos/{producto1_id}")
        print_response(response, "Producto Eliminado (404)")
        
        # 15. Lista final
        print("\n1️⃣5️⃣ Lista final de productos...")
        response = requests.get(f"{BASE_URL}/api/v1/productos/")
        print_response(response, "Lista Final")
    
    print("\n✅ DEMO COMPLETADO")
    print("\n📚 Documentación disponible en:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    demo_api()
