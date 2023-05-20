from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from .models import Producto
from rest_framework import viewsets, permissions
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    #detail necesita un id
    # @action(detail=True, methods=['patch'])
    # def modificar_stock(self, request, pk=None):
    #     producto = get_object_or_404(pk)
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # user.set_password(serializer.validated_data['password'])
    #         producto.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                 status=status.HTTP_400_BAD_REQUEST)
    #
    # def get_serializer_class(self):
    #     serializer = super().get_serializer_class()
    #     if(self.action == 'update'):
    #         serializer = ProductoUpdateSerializer
    #
    #     return serializer


    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ProductoFilter
    # ordering_fields = ['dni', 'nombre_completo']
    # lookup_field = 'uuid'
