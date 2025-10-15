from django.contrib import admin
from .models import Egreso, Ingreso

# --- ModelAdmin para Egreso ---
@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la vista de lista del admin
    list_display = (
        'caja', 
        'egreso_monto', 
        'egreso_descripcion', 
        'egreso_fecha_hora'
    )
    
    # Filtros laterales para búsqueda rápida por fecha y caja
    list_filter = (
        'caja', 
        'egreso_fecha_hora'
    )
    
    # Campos que se pueden buscar
    search_fields = (
        'egreso_descripcion', 
        'caja__id' # Permite buscar por el ID de la caja
    )
    
    # Campos que se muestran como solo lectura (se establecen automáticamente)
    readonly_fields = ('egreso_fecha_hora',)
    
    # Ordenar por fecha y hora de forma descendente por defecto
    ordering = ('-egreso_fecha_hora',)

# --- ModelAdmin para Ingreso ---
@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la vista de lista del admin
    list_display = (
        'caja', 
        'ingreso_monto', 
        'ingreso_descripcion', 
        'ingreso_fecha_hora'
    )
    
    # Filtros laterales para búsqueda rápida por fecha y caja
    list_filter = (
        'caja', 
        'ingreso_fecha_hora'
    )
    
    # Campos que se pueden buscar
    search_fields = (
        'ingreso_descripcion', 
        'caja__id' # Permite buscar por el ID de la caja
    )
    
    # Campos que se muestran como solo lectura
    readonly_fields = ('ingreso_fecha_hora',)
    
    # Ordenar por fecha y hora de forma descendente por defecto
    ordering = ('-ingreso_fecha_hora',)