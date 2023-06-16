import pytest



from ecommerce_api.apps.core.tests.fixtures import api_client, get_default_test_user

from ecommerce_api.apps.orden.tests.fixtures import crear_orden, crear_producto


@pytest.mark.django_db
def test_api_crear_detalle_orden(api_client, crear_orden, crear_producto):
    client = api_client
    orden = crear_orden("2024-06-03T13:08:00Z")
    producto = crear_producto("leche", 1500,100)
    data = {
        "orden":orden.id,
        "cantidad": 5,
        "producto":producto.id
    }
    response = client.post('/api/v1/detalle_orden/', data=data)
    assert response.status_code == 201
    # orden = crear_orden("2022-06-03T13:08:00Z")
    # producto = crear_producto('leche',280,10)
    # detalle_orden = crear_detalle_orden(orden,3,producto)
    #
    # assert DetalleOrden.objects.count() == 1
    # #assert MyModel.objects.get(nombre="Ejemplo").descripcion == "Descripción de ejemplo"