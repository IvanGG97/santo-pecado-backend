from django.db import models

class Cliente(models.Model):
    cliente_dni = models.CharField(max_length=200, unique=True,null=True, blank=True)
    cliente_nombre = models.CharField(max_length=200)
    cliente_apellido = models.CharField(max_length=200,null=True, blank=True)
    cliente_telefono = models.CharField(max_length=200)
    cliente_direccion = models.CharField(max_length=200)
    cliente_email = models.EmailField(max_length=200,null=True, blank=True)


    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.cliente_nombre}"
