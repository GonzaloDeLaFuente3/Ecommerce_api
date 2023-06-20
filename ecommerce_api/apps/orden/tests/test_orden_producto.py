import json

import pytest
from django.urls import reverse

from apps.core.tests.fixtures import api_client , get_default_test_user
from apps.orden.models import DetalleOrden, Orden
from apps.producto.models import Producto
from apps.orden.tests.fixtures import crear_orden, crear_productos

# 5. Verificar que al ejecutar el endpoint de eliminación de una orden, ésta se haya
# eliminado de la base de datos correctamente, junto con su detalle, y que además, se
# haya incrementado el stock de producto relacionado con cada detalle de orden.

@pytest.mark.django_db
def test_api_eliminar_orden(api_client,crear_orden,crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos

    stock_inicial_p1 = producto1.stock
    stock_inicial_p2 = producto2.stock

    DetalleOrden.objects.create(orden=orden, cantidad=40, producto=producto1)
    DetalleOrden.objects.create(orden=orden, cantidad=60, producto=producto2)

    url = reverse('orden-detail', args=[orden.pk])
    response = client.delete(url, content_type='application/json')

    #Verificamos que la respuesta http es la correcta
    assert response.status_code == 204

    assert not DetalleOrden.objects.filter(
             orden=orden).exists(), "Los objetos DetalleOrden no se han eliminado correctamente de la base de datos"

    assert not Orden.objects.filter(pk=orden.pk
        ).exists(), "El objeto Orden no se ha eliminado correctamente de la base de datos"

    assert producto1.stock == stock_inicial_p1, "El stock inicial del producto 1 es diferente al final"

    assert producto2.stock == stock_inicial_p2, "El stock inicial del producto 1 es diferente al final"


# 6. Verificar que al ejecutar el endpoint de modificación del stock de un producto, actualiza
# correctamente dicho stock.

@pytest.mark.django_db
def test_api_modificar_stock_producto(api_client,crear_productos):
    client = api_client
    producto1, producto2 = crear_productos

    stock_inicial_p2 = producto2.stock

    # Datos de modificación del stock
    data = {
        "nombre": "",
        "precio": "",
        "stock": 50
    }

    url = reverse('producto-modificar-stock', args=[producto1.pk])
    response = client.patch(url, data=data)

    # Verificamos que la respuesta http es la correcta
    assert response.status_code == 200

    # Verificar que el stock del producto1 se haya modificado correctamente en la base de datos
    producto1_actualizado = Producto.objects.get(pk=producto1.pk)
    assert producto1_actualizado.stock == data['stock']

    # Verificar que el stock del producto2 no haya sido modificado
    producto2_actualizado = Producto.objects.get(pk=producto2.pk)
    assert producto2_actualizado.stock == stock_inicial_p2


# 7. Verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo
# al total de cada detalle.

@pytest.mark.django_db
def test_api_get_total_orden(crear_orden,crear_productos):
    orden = crear_orden
    producto1, producto2 = crear_productos

    # Crear instancias de DetalleOrden y asociarlas a la Orden
    detalle_orden1 = DetalleOrden.objects.create(orden=orden, cantidad=40, producto=producto1)
    detalle_orden2 = DetalleOrden.objects.create(orden=orden, cantidad=60, producto=producto2)

    # Calcular el total esperado
    total_esperado = (detalle_orden1.producto.precio * detalle_orden1.cantidad) + \
                     (detalle_orden2.producto.precio * detalle_orden2.cantidad)

    # Obtener el total utilizando el método get_total() de la Orden
    total_obtenido = orden.get_total()

    # Verificar que el total obtenido es igual al total esperado
    assert total_obtenido == total_esperado

# 8. Verificar que el método get_total_detalle de un detalle de orden, devuelve el valor
# correcto de acuerdo a al precio del producto y cantidad de la orden.