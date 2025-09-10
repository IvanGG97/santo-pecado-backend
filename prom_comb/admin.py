from django.contrib import admin
from .models import Promocion, Combo, Producto_Combo, Producto_Promocion

# Register your models here.

class Producto_ComboInline(admin.TabularInline):
    model = Producto_Combo
    extra = 1
    autocomplete_fields = ('producto',)


class ComboAdmin(admin.ModelAdmin):
    list_display = ('combo_nombre', 'combo_precio')
    list_display_links = ('combo_nombre',)
    search_fields = ('combo_nombre',)
    list_per_page = 25
    ordering = ('combo_nombre',)
    inlines = [Producto_ComboInline]

admin.site.register(Combo, ComboAdmin)


class Producto_ComboAdmin(admin.ModelAdmin):
    list_display = ('combo', 'producto', 'producto_combo_cantidad', 'producto_combo_precio')
    list_display_links = ('combo', 'producto')
    search_fields = ('combo__combo_nombre', 'producto__producto_nombre')
    list_filter = ('combo',)
    list_per_page = 25
    autocomplete_fields = ('combo', 'producto')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('combo', 'producto')

admin.site.register(Producto_Combo, Producto_ComboAdmin)


class Producto_PromocionInline(admin.TabularInline):
    model = Producto_Promocion
    extra = 1
    autocomplete_fields = ('producto',)


class PromocionAdmin(admin.ModelAdmin):
    list_display = ('promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 'promocion_fecha_hora_fin', 'esta_activa')
    list_display_links = ('promocion_nombre',)
    search_fields = ('promocion_nombre',)
    list_filter = ('promocion_fecha_hora_inicio', 'promocion_fecha_hora_fin')
    list_per_page = 25
    ordering = ('-promocion_fecha_hora_inicio',)
    inlines = [Producto_PromocionInline]
    
    def esta_activa(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.promocion_fecha_hora_inicio <= now <= obj.promocion_fecha_hora_fin
    esta_activa.boolean = True
    esta_activa.short_description = 'Activa'

admin.site.register(Promocion, PromocionAdmin)


class Producto_PromocionAdmin(admin.ModelAdmin):
    list_display = ('promocion', 'producto', 'producto_promocion_cantidad', 'producto_promocion_precio', 'get_promocion_fecha_inicio', 'get_promocion_fecha_fin')
    list_display_links = ('promocion', 'producto')
    search_fields = ('promocion__promocion_nombre', 'producto__producto_nombre')
    list_filter = ('promocion',)
    list_per_page = 25
    autocomplete_fields = ('promocion', 'producto')
    
    def get_promocion_fecha_inicio(self, obj):
        return obj.promocion.promocion_fecha_hora_inicio
    get_promocion_fecha_inicio.short_description = 'Inicio Promoción'
    get_promocion_fecha_inicio.admin_order_field = 'promocion__promocion_fecha_hora_inicio'
    
    def get_promocion_fecha_fin(self, obj):
        return obj.promocion.promocion_fecha_hora_fin
    get_promocion_fecha_fin.short_description = 'Fin Promoción'
    get_promocion_fecha_fin.admin_order_field = 'promocion__promocion_fecha_hora_fin'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('promocion', 'producto')

admin.site.register(Producto_Promocion, Producto_PromocionAdmin)