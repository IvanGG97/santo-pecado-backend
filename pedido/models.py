from django.db import models
from inventario.models import Producto
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
    pedido_fecha=models.DateTimeField(auto_now_add=True)
    pedido_hora=models.TimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural='Pedidos'
        verbose_name="Pedido"
    def __str__(self):
        return self.estado_pedido.estado_pedido_nombre
    
class Detalle_Pedido(models.Model):
    pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural='Detalles de pedidos'
        verbose_name="Detalle de pedido"
    def __str__(self):
        return self.producto.producto_nombre
    