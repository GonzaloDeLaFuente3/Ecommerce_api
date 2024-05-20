import pytest

from apps.orden.models import Orden, DetalleOrden
from apps.producto.models import Producto

@pytest.fixture
def crear_orden():
    orden, _ = Orden.objects.get_or_create(
        defaults={
            'fecha_hora': "2024-06-03T13:08:00Z"
        }
    )
    return orden

def crear_producto(nombre,precio,stock):
    producto, _ = Producto.objects.get_or_create(
        nombre=nombre,
        precio=precio,
        stock=stock
    )
    return producto
@pytest.fixture
def crear_productos():
    producto1 = crear_producto("leche",1500,100)
    producto2 = crear_producto("Helado",500,900)
    return producto1, producto2

@pytest.fixture
def producto_cargado():
    return crear_producto('Almendras', 300, 1000)