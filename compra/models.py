from django.db import models

# Create your models here.
class Compra(models.Model):
    proveedor=models.ForeignKey("proveedor.Proveedor",on_delete=models.CASCADE)
    empleado=models.ForeignKey("empleado.Empleado",on_delete=models.CASCADE)
    caja=models.ForeignKey("caja.Caja",on_delete=models.CASCADE)
    compra_fecha_hora=models.DateTimeField()
    compra_total=models.FloatField()

    class Meta:
        verbose_name="Compra"
        verbose_name_plural="Compras"

    def __str__(self):
        return f"Compra N°{self.id}"
    
class Detalle_Compra(models.Model):
    compra=models.ForeignKey(Compra, on_delete=models.CASCADE)
    insumo=models.ForeignKey("inventario.Insumo",on_delete=models.CASCADE)
    detalle_compra_cantidad=models.FloatField()
    detalle_compra_precio_unitario=models.FloatField()


    class Meta:
        verbose_name="Detalle de Compra"
        verbose_name_plural="Detalles de Compras"

    def __str__(self):
        return f"Detalle de Compra N°{self.compra}"

    
