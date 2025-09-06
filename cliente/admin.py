from django.contrib import admin
from .models import *
# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','cliente_dni','cliente_nombre','cliente_apellido','cliente_telefono','cliente_direccion')
admin.site.register(Cliente,ClienteAdmin)
