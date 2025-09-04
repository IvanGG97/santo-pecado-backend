from django.db import models

# Create your models here.
class Proveedor(models.Model):
    proveedor_dni= models.CharField(max_length=100,unique=True)
    proveedor_nombre = models.CharField(max_length=100)
    proveedor_direccion = models.CharField(max_length=200)
    proveedor_telefono = models.CharField(max_length=20)
    proveedor_email = models.EmailField()
    
    class Meta:
        verbose_name_plural = "Proveedores"
        verbose_name = "Proveedor"
    
    def __str__(self):
        return self.proveedor_nombre