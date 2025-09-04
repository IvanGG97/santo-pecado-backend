from django.db import models

# Create your models here.

class Estado_Pedido(models.Model):
    estado_pedido_nombre=models.CharField(max_length=200)

    class Meta:
        verbose_name_plural='Estados de pedidos'
        verbose_name="Estado de pedido"

    def __str__(self):
        return self.estado_pedido_nombre
    

class Pedido(models.Model):
    estado_pedido=models.ForeignKey(Estado_Pedido,on_delete=models.CASCADE)
    