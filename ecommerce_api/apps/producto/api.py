from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Producto
from rest_framework import viewsets, permissions, status
from .serializers import ProductoSerializer, ProductoUpdateSerializer, ProductoStockSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # detail necesita un id
    # no me salio todavia
    @action(detail=True, methods=['patch'])
    def modificar_stock(self, request, pk=None):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoStockSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            # user.set_password(serializer.validated_data['password'])
            serializer.save()
            return Response({'status': 'stock updated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    # lo de abajo esta bien ya
    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if(self.action == 'update'):
            serializer = ProductoUpdateSerializer

        return serializer


    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductoFilter
    # ordering_fields = ['dni', 'nombre_completo']
    # lookup_field = 'uuid'
