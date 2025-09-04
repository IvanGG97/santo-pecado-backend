from django.db import models

# Create your models here.
class Estado_Venta(models.Model):
    estado_venta_nombre=models.CharField(max_length=200)

    class Meta:
        verbose_name="Estado de Venta"
        verbose_name_plural="Estados de Ventas"

    def __str__(self):
        return self.estado_venta_nombre
    

class Venta(models.Model):
    cliente=models.ForeignKey("cliente.Cliente",on_delete=models.CASCADE)
    empleado=models.ForeignKey("empleado.Empleado",on_delete=models.CASCADE)
    caja=models.ForeignKey("caja.Caja",on_delete=models.CASCADE)
    pedido=models.ForeignKey("pedido.Pedido",on_delete=models.CASCADE)
    estado_venta=models.ForeignKey(Estado_Venta,on_delete=models.CASCADE)
    venta_fecha_hora=models.DateTimeField()
    venta_total=models.FloatField()
    venta_medio_pago=models.CharField(max_length=200)
    venta_descuento=models.FloatField(default=0)

    class Meta:
        verbose_name="Venta"
        verbose_name_plural="Ventas"

    def __str__(self):
        return f"Venta N°{self.id}"