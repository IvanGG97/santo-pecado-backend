from django.db import models
from caja.models import Caja
# Create your models here.
class Egreso(models.Model):
    caja=models.ForeignKey(Caja, on_delete=models.CASCADE)
    egreso_descripcion=models.CharField(max_length=200)
    egreso_monto=models.FloatField()
    egreso_fecha_hora=models.DateTimeField()

    class Meta:
        verbose_name="Egreso"
        verbose_name_plural="Egresos"

    def __str__(self):
        return f"Egreso:{self.egreso_monto} de la Caja {self.caja}"
    

class Ingreso(models.Model):
    caja=models.ForeignKey(Caja, on_delete=models.CASCADE)
    ingreso_descripcion=models.CharField(max_length=200)
    ingreso_monto=models.FloatField()
    ingreso_fecha_hora=models.DateTimeField()

    class Meta:
        verbose_name="ingreso"
        verbose_name_plural="ingresos"

    def __str__(self):
        return f"ingreso:{self.ingreso_monto} a la Caja {self.caja}"