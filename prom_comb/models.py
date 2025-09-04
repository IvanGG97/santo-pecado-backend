from django.db import models

# Create your models here.
class Promocion(models.Model):
    promocion_nombre = models.CharField(max_length=100)
    promocion_precio = models.FloatField()
    promocion_fecha_hora_inicio = models.DateTimeField()
    promocion_fecha_hora_fin = models.DateTimeField()

    class Meta:
        verbose_name = 'Promocion'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return self.promocion_nombre
    
class Combo(models.Model):
    combo_nombre = models.CharField(max_length=200)
    combo_precio = models.FloatField()

    class Meta:
        verbose_name = 'Combo'
        verbose_name_plural = 'Combos'

    def __str__(self):
        return self.combo_nombre
    
class Producto_Combo(models.Model):
    producto = models.ForeignKey("inventario.Producto", on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    producto_combo_cantidad = models.IntegerField()
    producto_combo_precio = models.FloatField()

    class Meta:
        verbose_name = 'Producto Combo'
        verbose_name_plural = 'Productos Combos'

    def __str__(self):
        return self.producto.nombre
    
class Producto_Promocion(models.Model):
    producto = models.ForeignKey("inventario.Producto", on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    producto_promocion_cantidad = models.IntegerField()
    producto_promocion_precio = models.FloatField()

    class Meta:
        verbose_name = 'Producto Promocion'
        verbose_name_plural = 'Productos Promociones'
    
    def __str__(self):
        return self.producto.nombre
   