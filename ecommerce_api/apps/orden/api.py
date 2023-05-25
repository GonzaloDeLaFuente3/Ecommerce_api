
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from .models import Orden, DetalleOrden
import requests
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions
from .serializers import OrdenSerializer, DetalleOrdenSerializer


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

    # convocar al metodo get_total, obtener el total y luego cuando lo quiera obtener en dolares
    # lo envio y hago las comparaciones, etc...
    @action(detail=True, methods=['get'])
    def get_total_usd(self, request, pk=None):
        orden = get_object_or_404(Orden, pk=pk)
        total = orden.get_total()
        response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        total_usd = total / (float(response.json()[1]["casa"]["venta"].replace(',','.')))

        return Response({'precio_usd':round(total_usd,2)})


class DetalleOrdenViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer


    def perform_create(self, serializer):
        producto = serializer.validated_data.get('producto', None)
        cantidad = serializer.validated_data.get('cantidad', None)
        orden = serializer.validated_data.get('orden', None)
        # para pedidos no utlicé self.queryset porque se
        # quedaba guardada la queryset anterior y no funcionaba bien
        pedidos = DetalleOrden.objects.all()

        # VALIDACIONES: Cualquier validacion que no se cumpla
        # inmediatamente deja de ejecutar el método de manera
        # que no se podrá crear un registro sin antes pasar por
        # estas validaciones

        # Validacion cantidad de productos mayor a 0
        if cantidad <= 0:
            raise ValidationError('La cantidad del producto debe ser mayor a 0')

        # Validacion stock suficiente
        if cantidad > producto.stock:
            raise ValidationError('No hay stock suficiente')

        # Validacion para que no se repitan productos en el mismo pedido
        for pedido in pedidos:
            if pedido.orden == orden and pedido.producto == producto:
                raise ValidationError('Este producto ya existe en el pedido. No se pueden repetir los mismos')

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


    def delete(self, request, pk, format=None):
        detalle_orden = get_object_or_404(DetalleOrden.objects.all(), pk=pk)
        producto = self.get_object().producto
        cantidad = self.get_object().cantidad
        producto.stock += cantidad
        producto.save()
        detalle_orden.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

