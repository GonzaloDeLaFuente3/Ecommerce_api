import pytest

from apps.core.tests.fixtures import api_client , get_default_test_user
from apps.orden.models import DetalleOrden
from apps.orden.tests.fixtures import crear_orden, crear_productos


from apps.producto.models import Producto

# verifico que el endpoint de crear un detalle orden se cree correctamente
# verifico que se actualice el stock del producto
# verifico que no se pueda crear un detalle orden si la cantidad superar el stock disponible
@pytest.mark.parametrize(
    'cantidad, codigo_http,total_registros,disponible_stock',
    [(5,201,1,True),
     (99,201,1,True),
     (100,201,1,True),
     (101,400,0,False),
     (200,400,0,False)]
)
@pytest.mark.django_db
def test_api_crear_detalle_orden(api_client, crear_orden, crear_productos,
                                 cantidad,codigo_http,total_registros,disponible_stock):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    stock_anterior = producto1.stock  # Stock del producto antes de crear el detalle de la orden
    data = {
        "orden": orden.pk,
        "cantidad": cantidad,
        "producto": producto1.pk
    }
    response = client.post('/api/v1/detalle_orden/', data=data)
    assert response.status_code == codigo_http
    assert DetalleOrden.objects.filter(orden=orden, cantidad=cantidad, producto=producto1).count() == total_registros
    producto1_actualizado = Producto.objects.get(pk=producto1.pk)
    if disponible_stock:
        assert producto1_actualizado.stock == stock_anterior - cantidad
    if not disponible_stock:
        assert producto1_actualizado.stock == 100





#verifica que la recuperacion de los detalles orden sean correcta
@pytest.mark.django_db
def test_api_recuperar_detalle_orden(api_client,crear_orden,crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    data = {
        "orden":orden.pk,
        "cantidad": 5,
        "producto":producto1.pk
    }
    response_crear = client.post('/api/v1/detalle_orden/', data=data)
    assert response_crear.status_code == 201
    data1 = {
        "orden": orden.pk,
        "cantidad": 10,
        "producto": producto2.pk
    }
    response_crear2 = client.post('/api/v1/detalle_orden/', data=data1)
    assert response_crear2.status_code == 201
    response = client.get('/api/v1/detalle_orden/')
    assert response.status_code == 200
    json_data = response.json()
    assert len(json_data) == 2
    assert json_data[0]['orden'] == orden.pk
    assert json_data[0]['cantidad'] == 5
    assert json_data[0]['producto'] == producto1.pk
    assert json_data[1]['orden'] == orden.pk
    assert json_data[1]['cantidad'] == 10
    assert json_data[1]['producto'] == producto2.pk

#verifica que de un codigo 400 al intentar tener dos productos iguales
@pytest.mark.django_db
def test_api_crear_detalle_orden_productos_repetidos(api_client,crear_orden,crear_productos):
    client = api_client
    orden = crear_orden
    producto1, producto2 = crear_productos
    data = {
        "orden":orden.pk,
        "cantidad": 5,
        "producto":producto1.pk
    }
    response_crear = client.post('/api/v1/detalle_orden/', data=data)
    assert response_crear.status_code == 201
    data1 = {
        "orden": orden.pk,
        "cantidad": 10,
        "producto": producto1.pk
    }
    response_crear2 = client.post('/api/v1/detalle_orden/', data=data1)
    assert response_crear2.status_code == 400


