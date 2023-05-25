
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from .models import Orden, DetalleOrden
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions
from .serializers import OrdenSerializer, DetalleOrdenSerializer


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer


class DetalleOrdenViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer


    def perform_create(self, serializer):
        producto = serializer.validated_data.get('producto', None)
        cantidad = serializer.validated_data.get('cantidad', None)

        if cantidad > producto.stock or cantidad <= 0:
            raise ValidationError('No hay stock suficiente')
        else:
            producto.stock -= cantidad
            producto.save()
            super().perform_create(serializer)


    # Modificar
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Verificar y actualizar el stock en Producto
        nueva_cantidad = serializer.validated_data.get('cantidad', None)
        if nueva_cantidad is not None:
            producto = instance.producto
            cantidad_anterior = instance.cantidad

            if nueva_cantidad > (producto.stock + cantidad_anterior):
                return Response({'error': 'La cantidad no puede ser mayor al stock disponible.'}, status=status.HTTP_400_BAD_REQUEST)

            bandera = False
            if nueva_cantidad > cantidad_anterior:
                bandera = True
            if bandera:
                #aumenta
                producto.stock -= (nueva_cantidad - cantidad_anterior)
                producto.save()
            else:
                #disminuye
                producto.stock += (cantidad_anterior - nueva_cantidad)
                producto.save()

        super().update(request, *args, **kwargs)

        return Response(serializer.data)


    #Eliminar, falta modificacion
    def delete(self, request, pk, format=None):
        detalle_orden = get_object_or_404(DetalleOrden.objects.all(), pk=pk)
        detalle_orden.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

