import pytest
from django.urls import reverse

from apps.core.tests.fixtures import api_client , get_default_test_user
from apps.orden.models import DetalleOrden, Orden
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

    data = {
        "orden":orden.pk,
        "cantidad": 40,
        "producto":producto1.pk
    }
    data2 = {
        "orden": orden.pk,
        "cantidad": 60,
        "producto": producto2.pk
    }

    client.post('/api/v1/detalle_orden/', data=data)
    client.post('/api/v1/detalle_orden/', data=data2)

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


# 7. Verificar que el método get_total de una orden, devuelve el valor correcto de acuerdo
# al total de cada detalle.


# 8. Verificar que el método get_total_detalle de un detalle de orden, devuelve el valor
# correcto de acuerdo a al precio del producto y cantidad de la orden.