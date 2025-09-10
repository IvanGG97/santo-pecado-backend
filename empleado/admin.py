from django.contrib import admin
from .models import Rol_Empleado,Empleado
# Register your models here.

class Rol_EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id','rol_nombre')
admin.site.register(Rol_Empleado,Rol_EmpleadoAdmin)


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('rol_empleado','empleado_dni','empleado_nombre','empleado_apellido','empleado_telefono')
admin.site.register(Empleado,EmpleadoAdmin)

