from rest_framework import serializers
from .models import Orden, DetalleOrden

class OrdenSerializer(serializers.ModelSerializer):
    total_pedido = serializers.SerializerMethodField(method_name='obtener_total_pedido')
    class Meta:
        model = Orden
        fields = '__all__'
        read_only_fields = ['total_pedido']

    def obtener_total_pedido(self, obj):
        return obj.get_total()

class DetalleOrdenSerializer(serializers.ModelSerializer):
    total_detalle = serializers.SerializerMethodField(method_name='obtener_total_detalle')
    class Meta:
        model = DetalleOrden
        fields = '__all__'
        read_only_fields = ['total_detalle']

    def obtener_total_detalle(self, obj):
        return obj.get_total_detalle()
