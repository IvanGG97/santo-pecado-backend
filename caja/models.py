from django.db import models

# Create your models here.
class Caja(models.Model):
    caja_estado=models.BooleanField(default=True)
    caja_monto_inicial=models.FloatField(default=0)
    caja_saldo_final=models.FloatField(default=0,null=True,blank=True)
    caja_fecha_hora_apertura=models.DateTimeField(auto_now=True)
    caja_fecha_hora_cierre=models.DateTimeField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural="Cajas"
        verbose_name="Caja"
    def __str__(self):
        return str(self.caja_monto_inicial)
    
    
