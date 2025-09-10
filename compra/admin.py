from django.contrib import admin
from .models import Proveedor, Compra,Detalle_Compra
# Register your models here.
class ProveedorAdmin(admin.ModelAdmin):
    list_display=('proveedor_dni','proveedor_nombre','proveedor_direccion','proveedor_telefono','proveedor_email')
admin.site.register(Proveedor,ProveedorAdmin)

class CompraAdmin(admin.ModelAdmin):
    list_display=('proveedor','empleado','caja','compra_fecha_hora','compra_total','compra_metodo_pago')
admin.site.register(Compra,CompraAdmin)

class Detalle_CompraAdmin(admin.ModelAdmin):
    list_display=('compra','insumo','detalle_compra_cantidad','detalle_compra_precio_unitario')
admin.site.register(Detalle_Compra,Detalle_CompraAdmin)