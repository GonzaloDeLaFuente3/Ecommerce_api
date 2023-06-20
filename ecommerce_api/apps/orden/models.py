from datetime import datetime
from django.db import models

from apps.producto.models import Producto


# Create your models here.

class Orden(models.Model):

    fecha_hora = models.DateTimeField(default=datetime.today)

    def get_total(self):
        total = 0.0
        for detalle_orden in DetalleOrden.objects.filter(orden=self):
            total += detalle_orden.get_total_detalle()

        return total


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles_orden')
    cantidad = models.FloatField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_productos')

    def get_total_detalle(self):
        total = self.producto.precio * self.cantidad
        return total