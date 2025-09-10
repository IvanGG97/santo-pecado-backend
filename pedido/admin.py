from django.contrib import admin
from .models import Estado_Pedido, Pedido, Detalle_Pedido

# Register your models here.

class Estado_PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_pedido_nombre')
    list_display_links = ('id', 'estado_pedido_nombre')
    search_fields = ('estado_pedido_nombre',)
    list_per_page = 25

admin.site.register(Estado_Pedido, Estado_PedidoAdmin)


class Detalle_PedidoInline(admin.TabularInline):
    model = Detalle_Pedido
    extra = 1
    autocomplete_fields = ('producto',)


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado_pedido', 'pedido_fecha', 'pedido_hora')
    list_display_links = ('id',)
    list_filter = ('estado_pedido', 'pedido_fecha')
    search_fields = ('estado_pedido__estado_pedido_nombre',)
    list_per_page = 25
    ordering = ('-pedido_fecha', '-pedido_hora')
    readonly_fields = ('pedido_fecha', 'pedido_hora')
    inlines = [Detalle_PedidoInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('estado_pedido')

admin.site.register(Pedido, PedidoAdmin)


class Detalle_PedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'get_pedido_fecha', 'get_estado_pedido')
    list_display_links = ('pedido', 'producto')
    list_filter = ('pedido__estado_pedido', 'pedido__pedido_fecha')
    search_fields = ('producto__producto_nombre', 'pedido__id')
    list_per_page = 25
    autocomplete_fields = ('pedido', 'producto')
    
    def get_pedido_fecha(self, obj):
        return obj.pedido.pedido_fecha
    get_pedido_fecha.short_description = 'Fecha del Pedido'
    get_pedido_fecha.admin_order_field = 'pedido__pedido_fecha'
    
    def get_estado_pedido(self, obj):
        return obj.pedido.estado_pedido
    get_estado_pedido.short_description = 'Estado del Pedido'
    get_estado_pedido.admin_order_field = 'pedido__estado_pedido'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pedido__estado_pedido', 'producto')

admin.site.register(Detalle_Pedido, Detalle_PedidoAdmin)