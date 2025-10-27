from django.db import models
from inventario.models import Producto
from empleado.models import Empleado

class Estado_Pedido(models.Model):
    estado_pedido_nombre=models.CharField(max_length=200)
    class Meta:
        verbose_name_plural='Estados de pedidos'
        verbose_name="Estado de pedido"
    def __str__(self):
        return self.estado_pedido_nombre

class Pedido(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    estado_pedido=models.ForeignKey(Estado_Pedido,on_delete=models.CASCADE)
    pedido_fecha_hora=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='Pedidos'
        verbose_name="Pedido"
    def __str__(self):
        return f"Pedido N°{self.id} - {self.estado_pedido.estado_pedido_nombre}"

class Detalle_Pedido(models.Model):
    # Añadimos related_name para facilitar el acceso
    pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE, related_name='detalles')
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE, null=True, blank=True)
    
    # --- ¡CAMPOS AÑADIDOS! ---
    cantidad = models.PositiveIntegerField(default=1)
    # Guardamos el precio al momento de la venta para registros históricos
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    # Aquí guardamos las personalizaciones (ej: "Sin lechuga, sin tomate")
    notas = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural='Detalles de pedidos'
        verbose_name="Detalle de pedido"
    def __str__(self):
        if self.producto:
            return self.producto.producto_nombre
        # Si no hay producto, es una promoción. Usamos las notas como descripción.
        return self.notas or "Item de Promoción"