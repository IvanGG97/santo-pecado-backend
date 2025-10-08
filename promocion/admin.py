from django.contrib import admin
from .models import Promocion, Producto_Promocion

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('promocion_nombre', 'promocion_precio', 'promocion_stock', 
                   'promocion_fecha_hora_inicio', 'promocion_fecha_hora_fin', 
                   'esta_activa')
    list_filter = ('promocion_fecha_hora_inicio', 'promocion_fecha_hora_fin')
    search_fields = ('promocion_nombre', 'promocion_descripcion')
    readonly_fields = ('esta_activa',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('promocion_nombre', 'promocion_precio', 'promocion_stock')
        }),
        ('Fechas y Horarios', {
            'fields': ('promocion_fecha_hora_inicio', 'promocion_fecha_hora_fin'),
            'classes': ('collapse',)
        }),
        ('Descripción', {
            'fields': ('promocion_descripcion',),
            'classes': ('collapse',)
        }),
    )
    
    def esta_activa(self, obj):
        from django.utils import timezone
        now = timezone.now()
        if obj.promocion_fecha_hora_inicio and obj.promocion_fecha_hora_fin:
            return obj.promocion_fecha_hora_inicio <= now <= obj.promocion_fecha_hora_fin
        return False
    esta_activa.boolean = True
    esta_activa.short_description = '¿Activa?'

@admin.register(Producto_Promocion)
class ProductoPromocionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'promocion')
    list_filter = ('promocion',)
    search_fields = ('producto__nombre', 'promocion__promocion_nombre')  # Ajusta 'producto__nombre' según tu modelo Producto
    autocomplete_fields = ('producto', 'promocion')