import pytest

from apps.core.tests.fixtures import api_client , get_default_test_user
from apps.orden.models import DetalleOrden
from apps.orden.tests.fixtures import crear_orden, crear_productos


@pytest.mark.django_db
def test_api_crear_detalle_orden(api_client,crear_orden,crear_productos):
    client = api_client
    orden = crear_orden
    programa1, programa2 = crear_productos
    data = {
        "orden":orden.pk,
        "cantidad": 5,
        "producto":programa1.pk
    }
    response = client.post('/api/v1/detalle_orden/', data=data)
    assert response.status_code == 201
    assert DetalleOrden.objects.filter(
             orden=orden, cantidad=5, producto=programa1
         ).count() == 1