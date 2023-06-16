import pytest

from apps.orden.models import Orden, DetalleOrden
from apps.producto.models import Producto


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

