from django.db import models

# Create your models here.
class Rol_Empleado(models.Model):
    rol_nombre = models.CharField(max_length=200)
    
    class Meta:
        verbose_name="Rol de empleado"
        verbose_name_plural = "Roles de empleados"
    def __str__(self):
        return self.rol_nombre
    



class Empleado(models.Model):
    rol_empleado=models.ForeignKey(Rol_Empleado,on_delete=models.CASCADE)
    empleado_dni=models.CharField(max_length=100,unique=True)
    empleado_nombre = models.CharField(max_length=30)
    empleado_apellido = models.CharField(max_length=30)
    empleado_telefono=models.CharField(max_length=100)


    class Meta:
        verbose_name="Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return self.empleado_nombre

