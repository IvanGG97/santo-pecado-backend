from django.db import models
# Create your models here.
class Tipo_Producto(models.Model):
    tipo_producto_nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Tipo de Producto'
        verbose_name_plural = 'Tipos de Productos'
    
    def __str__(self):
        return self.tipo_producto_nombre
    

class Categoria_Insumo(models.Model):
    categoria_insumo_nombre=models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Categoría de Insumo'
        verbose_name_plural = 'Categorías de Insumos'
    
    def __str__(self):
        return self.categoria_insumo_nombre
    

class Producto(models.Model):
    tipo_producto=models.ForeignKey(Tipo_Producto, on_delete=models.CASCADE)
    producto_nombre=models.CharField(max_length=200)
    producto_descripcion=models.CharField(max_length=200)
    producto_precio=models.DecimalField(max_digits=10, decimal_places=2)
    producto_disponible=models.BooleanField(default=True)
    producto_fecha_hora_creacion=models.DateTimeField(auto_now_add=True)
    producto_imagen=models.ImageField(upload_to='inventario/images', blank=True, null=True)
    
    def __str__(self):
        return self.producto_nombre
    class Meta:
        verbose_name_plural="Productos"
        verbose_name="Producto"

class Insumo(models.Model):
    categoria_insumo=models.ForeignKey(Categoria_Insumo, on_delete=models.CASCADE)
    insumo_nombre=models.CharField(max_length=200)
    insumo_unidad=models.CharField(max_length=50) # Ej: 'kg', 'litro', 'unidad'
    insumo_stock=models.DecimalField(max_digits=10, decimal_places=2)
    insumo_stock_minimo=models.DecimalField(max_digits=10, decimal_places=2)
    insumo_precio_compra=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.insumo_nombre
    class Meta:
        verbose_name_plural="Insumos"
        verbose_name="Insumo"

class Producto_X_Insumo(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    insumo=models.ForeignKey(Insumo, on_delete=models.CASCADE)
    producto_insumo_cantidad=models.DecimalField(max_digits=10, decimal_places=3)
    
    def __str__(self):
        return f'{self.producto.producto_nombre} - {self.insumo.insumo_nombre}'
    class Meta:
        verbose_name_plural="Productos por Insumos"
        verbose_name="Producto por Insumo"
