from .models import Orden, DetalleOrden
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions
from .serializers import OrdenSerializer, DetalleOrdenSerializer


class OrdenViewSet(viewsets.ModelViewSet):


    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer

    def perform_create(self, serializer):
        producto = serializer.validated_data.get('producto', None)
        cantidad = serializer.validated_data.get('cantidad', None)
        mensaje = ""

        if producto.stock < 1 or cantidad <= 0:
            raise ValidationError(
                'El producto seleccionado no cuenta con stock disponible. Seleccione otro producto')

        super().perform_create(serializer)
