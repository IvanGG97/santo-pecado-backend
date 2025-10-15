from django.contrib import admin
from .models import Cliente

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_apellido', 'cliente_dni', 'cliente_telefono', 'cliente_email')
    list_display_links = ('id', 'cliente_nombre')
    search_fields = ('cliente_nombre', 'cliente_apellido', 'cliente_dni')
    ordering = ('cliente_apellido', 'cliente_nombre')
    list_per_page = 20

