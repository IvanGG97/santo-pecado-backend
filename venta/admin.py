from django.contrib import admin
from .models import Estado_Venta, Venta, Detalle_Venta

# Register your models here.

class Estado_VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_venta_nombre')
    list_display_links = ('id', 'estado_venta_nombre')
    search_fields = ('estado_venta_nombre',)
    list_per_page = 25

admin.site.register(Estado_Venta, Estado_VentaAdmin)


class Detalle_VentaInline(admin.TabularInline):
    model = Detalle_Venta
    extra = 1
    # Removemos autocomplete_fields hasta que los modelos relacionados tengan search_fields
    # autocomplete_fields = ('producto',)
    readonly_fields = ('detalle_venta_precio_precio_unitario',)


class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'empleado', 'estado_venta', 'venta_fecha_hora', 'venta_total', 'venta_medio_pago', 'venta_descuento')
    list_display_links = ('id',)
    search_fields = ('cliente__cliente_nombre', 'cliente__cliente_apellido', 'empleado__empleado_nombre', 'empleado__empleado_apellido')
    list_filter = ('estado_venta', 'venta_fecha_hora', 'venta_medio_pago', 'caja')
    list_per_page = 25
    ordering = ('-venta_fecha_hora',)
    readonly_fields = ('venta_total',)
    inlines = [Detalle_VentaInline]
    # Removemos autocomplete_fields hasta que los modelos relacionados tengan search_fields definidos
    # autocomplete_fields = ('cliente', 'empleado', 'caja', 'pedido', 'estado_venta')
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('cliente', 'empleado', 'caja', 'pedido', 'estado_venta')
        }),
        ('Datos de la Venta', {
            'fields': ('venta_fecha_hora', 'venta_total', 'venta_medio_pago', 'venta_descuento')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'cliente', 'empleado', 'caja', 'pedido', 'estado_venta'
        )

admin.site.register(Venta, VentaAdmin)


class Detalle_VentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'detalle_venta_cantidad', 'detalle_venta_precio_precio_unitario', 'detalle_venta_descuento', 'get_venta_total', 'get_venta_fecha')
    list_display_links = ('venta', 'producto')
    search_fields = ('venta__id', 'producto__producto_nombre')
    list_filter = ('venta__estado_venta', 'venta__venta_fecha_hora')
    list_per_page = 25
    # Removemos autocomplete_fields hasta que los modelos relacionados tengan search_fields
    # autocomplete_fields = ('venta', 'producto')
    
    def get_venta_total(self, obj):
        return obj.venta.venta_total
    get_venta_total.short_description = 'Total Venta'
    get_venta_total.admin_order_field = 'venta__venta_total'
    
    def get_venta_fecha(self, obj):
        return obj.venta.venta_fecha_hora
    get_venta_fecha.short_description = 'Fecha Venta'
    get_venta_fecha.admin_order_field = 'venta__venta_fecha_hora'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'venta__estado_venta', 'producto', 'venta'
        )

admin.site.register(Detalle_Venta, Detalle_VentaAdmin)