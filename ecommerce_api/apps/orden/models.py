from datetime import datetime

from django.db import models

from apps.producto.models import Producto


# Create your models here.

class Orden(models.Model):

    fecha_hora = models.DateTimeField(default=datetime.today)



class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles_orden')
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_productos')