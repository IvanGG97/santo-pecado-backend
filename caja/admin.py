from django.contrib import admin
from .models import Caja

# Register your models here.
class CajaAdmin(admin.ModelAdmin):
    list_display = ('id', 'caja_estado', 'caja_monto_inicial', 'caja_saldo_final','caja_fecha_hora_apertura','caja_fecha_hora_cierre')

admin.site.register(Caja, CajaAdmin)