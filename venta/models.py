from django.db import models
from cliente.models import Cliente
from empleado.models import Empleado
from caja.models import Caja
from pedido.models import Pedido
from inventario.models import Producto
# Create your models here.


class Estado_Venta(models.Model):
    estado_venta_nombre=models.CharField(max_length=200)

    class Meta:
        verbose_name="Estado de Venta"
        verbose_name_plural="Estados de Ventas"

    def __str__(self):
        return self.estado_venta_nombre
    

class Venta(models.Model):
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    empleado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
    caja=models.ForeignKey(Caja,on_delete=models.CASCADE)
    pedido=models.ForeignKey(Pedido,on_delete=models.SET_NULL, null=True, blank=True)
    estado_venta=models.ForeignKey(Estado_Venta,on_delete=models.CASCADE)
    venta_fecha_hora=models.DateTimeField(auto_now_add=True)
    venta_total=models.DecimalField(max_digits=10, decimal_places=2)
    MEDIO_PAGO_CHOICES = (
        ('efectivo', 'Efectivo'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia', 'Transferencia'),
    )
    venta_medio_pago=models.CharField(max_length=20, choices=MEDIO_PAGO_CHOICES, default='efectivo')
    venta_descuento=models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name="Venta"
        verbose_name_plural="Ventas"

    def __str__(self):
        return f"Venta N°{self.id}"
    
class Detalle_Venta(models.Model):
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    venta=models.ForeignKey(Venta,on_delete=models.CASCADE)
    detalle_venta_cantidad=models.IntegerField()
    detalle_venta_precio_unitario=models.DecimalField(max_digits=10, decimal_places=2)
    detalle_venta_descuento=models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name="Detalle de Venta"
        verbose_name_plural="Detalles de Ventas"

    def __str__(self):
        return f"Detalle de Venta N°{self.id}"