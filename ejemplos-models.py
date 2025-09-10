class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField()
    hora_pedido = models.TimeField()
    estado_pedido = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora_creacion_pedido = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'


class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=255)
    descripcion_producto = models.TextField(blank=True, null=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    disponible_producto = models.IntegerField(blank=True, null=True)
    fecha_hora_creacion_producto = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class ProductosXPedidos(models.Model):
    pk = models.CompositePrimaryKey('id_producto', 'id_pedido')
    id_producto = models.ForeignKey(Productos, models.DO_NOTHING, db_column='id_producto')
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos_x_pedidos'


class Ventas(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido')
    fecha_venta = models.DateField()
    hora_venta = models.TimeField()
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    estado_venta = models.CharField(max_length=50, blank=True, null=True)
    fecha_hora_creacion_venta = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas'