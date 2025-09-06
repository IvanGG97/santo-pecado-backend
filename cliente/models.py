from django.db import models

# Create your models here.
class Cliente(models.Model):
    cliente_dni= models.CharField(max_length=200,unique=True)
    cliente_nombre = models.CharField(max_length=200)
    cliente_apellido = models.CharField(max_length=200)
    cliente_telefono = models.CharField(max_length=200)
    cliente_direccion = models.CharField(max_length=200)

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

    def __str__(self):
        return self.cliente_nombre
    