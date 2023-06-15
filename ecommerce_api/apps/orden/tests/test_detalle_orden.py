import pytest

from Ecommerce_api.ecommerce_api.apps.orden.models import DetalleOrden
from Ecommerce_api.ecommerce_api.apps.orden.tests.fixtures import crear_orden, crear_producto, crear_detalle_orden


@pytest.mark.django_db
def test_api_verificar_detalle_orden():
    orden = crear_orden("2022-06-03T13:08:00Z")
    producto = crear_producto('leche',280,10)
    detalle_orden = crear_detalle_orden(orden,3,producto)

    assert DetalleOrden.objects.count() == 1
    #assert MyModel.objects.get(nombre="Ejemplo").descripcion == "Descripción de ejemplo"