from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio']

class ProductoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['stock']