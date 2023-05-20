from .models import Orden, DetalleOrden
from rest_framework import viewsets, permissions
from .serializers import OrdenSerializer, DetalleOrdenSerializer


class OrdenViewSet(viewsets.ModelViewSet):


    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class DetalleOrdenViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer

# class DetalleOrdenViewSet(APIView):
#     # Obtener
#     def get(self, request, pk, format=None):
#         persona = get_object_or_404(DetalleOrden.objects.all(), pk=pk)
#         serializer = PersonaSerializer(persona)
#         return Response(serializer.data)
#
#     # Modificar
#     def put(self, request, pk, format=None):
#         persona = get_object_or_404(Persona.objects.all(), pk=pk)
#         serializer = PersonaSerializer(persona, data=request.data)
#         if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     #Eliminar
#     def delete(self, request, pk, format=None):
#         persona = get_object_or_404(Persona.objects.all(), pk=pk)
#         persona.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
