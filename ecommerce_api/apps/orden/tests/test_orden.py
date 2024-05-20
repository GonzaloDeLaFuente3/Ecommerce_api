import pytest

from apps.orden.tests.fixtures import crear_orden

@pytest.mark.django_db
def test_crear_orden(crear_orden):
    assert crear_orden.fecha_hora == '2024-06-03T13:08:00Z'