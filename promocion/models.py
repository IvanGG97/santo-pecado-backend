from django.db import models

# Create your models here.
class Promocion(models.Model):
    promocion_nombre = models.CharField(max_length=100)
    promocion_precio = models.DecimalField(max_digits=10, decimal_places=2)
    promocion_fecha_hora_inicio = models.DateTimeField(blank=True, null=True)
    promocion_fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    promocion_stock= models.IntegerField()
    promocion_descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Promocion'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return self.promocion_nombre
    


class Producto_Promocion(models.Model):
    producto = models.ForeignKey("inventario.Producto", on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='productos_promocion')
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Producto Promocion'
        verbose_name_plural = 'Productos Promociones'
    
    def __str__(self):
        return f'Producto:{self.producto} Promocion:{self.promocion}'