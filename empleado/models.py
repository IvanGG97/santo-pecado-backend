from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Rol(models.Model):
    rol_nombre = models.CharField(max_length=200)
    
    class Meta:
        verbose_name="Rol"
        verbose_name_plural = "Roles"
    def __str__(self):
        return self.rol_nombre
    



class Empleado(models.Model):
    empleado_dni=models.CharField(max_length=100,unique=True)
    empleado_nombre = models.CharField(max_length=30)
    empleado_apellido = models.CharField(max_length=30)
    empleado_telefono=models.CharField(max_length=100)
    empleado_email=models.EmailField()
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='empleado')

    class Meta:
        verbose_name="Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return self.empleado_nombre

# Señal para crear automáticamente el perfil de empleado cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_empleado_desde_usuario(sender, instance, created, **kwargs):
    if created:
        # Extraer nombre y apellido del username o email
        nombre = instance.first_name or instance.username
        apellido = instance.last_name or ""
        
        Empleado.objects.create(usuario=instance,
            empleado_dni=instance.username,  
            empleado_nombre=nombre,
            empleado_apellido=apellido,
            empleado_email=instance.email,
            empleado_telefono="")
        

class Empleado_x_rol(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    rol=models.ForeignKey(Rol,on_delete=models.CASCADE)

    class Meta:
        verbose_name="Empleado por Rol"
        verbose_name_plural="Empleados por Roles"

    def __str__(self):
        return f"{self.rol}:{self.empleado}"