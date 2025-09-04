from django.db import models

# Create your models here.
class Caja(models.Model):
    caja_estado=models.BooleanField(default=True)
    caja_monto_inicial=models.FloatField(default=0)
    caja_saldo_final=models.FloatField(default=0)
    caja_fecha_hora_apertura=models.DateField(auto_now_add=True)
    caja_fecha_hora_cierre=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Cajas"
        verbose_name="Caja"
    def __str__(self):
        return str(self.caja_monto_inicial)
    
    
