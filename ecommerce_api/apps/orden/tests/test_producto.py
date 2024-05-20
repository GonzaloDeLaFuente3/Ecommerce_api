import pytest

from apps.orden.tests.fixtures import producto_cargado

@pytest.mark.django_db
def test_crear_producto(producto_cargado):
    assert producto_cargado.nombre == 'Almendras'
    assert producto_cargado.precio == 300
    assert producto_cargado.stock == 1000

@pytest.mark.django_db
def test_actualizacion_nombre_producto(producto_cargado):
        producto_cargado.nombre = "Nueces"
        producto_cargado.save()
        assert producto_cargado.nombre == "Nueces"
        
@pytest.mark.django_db
def test_actualizacion_stock_producto(producto_cargado):
    producto_cargado.stock -= 100
    producto_cargado.save()
    assert producto_cargado.stock == 900

@pytest.mark.django_db
def test_eliminacion_producto(producto_cargado):
        producto_cargado.delete()
        # Se intenta obtener el producto eliminado desde la base de datos
        with pytest.raises(producto_cargado.DoesNotExist):
            producto_cargado.refresh_from_db()

