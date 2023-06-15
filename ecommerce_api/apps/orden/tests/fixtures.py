from Ecommerce_api.ecommerce_api.apps.orden.models import Orden, DetalleOrden
from Ecommerce_api.ecommerce_api.apps.producto.models import Producto


def crear_orden(fecha):
    orden = Orden.objects.get_or_create(
        defaults={
            'fecha_hora': fecha
        }
    )
    return orden


def crear_producto(nombre, precio, stock):
    producto = Producto.objects.get_or_create(
        nombre=nombre,
        precio=precio,
        stock=stock
    )
    return producto

def crear_detalle_orden (orden:Orden, cantidad, producto:Producto):
    detalle_orden = DetalleOrden.objects.get_or_create(
        orden=orden,
        cantidad=cantidad,
        producto=producto
    )
