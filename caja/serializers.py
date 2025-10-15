from rest_framework import serializers
from .models import Caja
# Se asume que Empleado_x_rol tiene un __str__ que devuelve un nombre legible

class CajaSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre del Empleado y Rol asociado.
    # Se asume que Empleado_x_rol.__str__ o una propiedad de ese modelo
    # devuelve una representación legible (ej: "Juan Pérez - Cajero").
    empleado_rol_info = serializers.CharField(source='empleado_x_rol.__str__', read_only=True)

    class Meta:
        model = Caja
        fields = [
            'id', 
            'empleado_x_rol', 
            'empleado_rol_info', # Campo de solo lectura para la vista
            'caja_estado', 
            'caja_monto_inicial', 
            'caja_saldo_final', 
            'caja_fecha_hora_apertura', 
            'caja_fecha_hora_cierre', 
            'caja_observacion'
        ]
        # Hacemos estos campos de solo lectura para que la API los devuelva, pero no permita 
        # modificarlos directamente, ya que deben ser manejados por lógica de negocio.
        read_only_fields = ('caja_saldo_final', 'caja_fecha_hora_apertura')


    # Opcional: Validar que solo se puede abrir una caja por Empleado_x_Rol
    def validate(self, data):
        empleado_x_rol = data.get('empleado_x_rol')

        # Si se está intentando abrir una nueva caja (POST)
        if not self.instance and empleado_x_rol:
            # Comprueba si ya existe una caja abierta para este Empleado_x_Rol
            caja_abierta = Caja.objects.filter(
                empleado_x_rol=empleado_x_rol, 
                caja_estado=True
            ).exists()
            
            if caja_abierta:
                raise serializers.ValidationError(
                    "Ya existe una caja abierta para este Empleado y Rol. Debe cerrarla antes de abrir una nueva."
                )
        
        return data