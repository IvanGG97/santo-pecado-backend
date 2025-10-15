from rest_framework import serializers
from .models import Egreso, Ingreso
# Importamos el modelo Caja para la validación avanzada
from caja.models import Caja 

# --- Serializer Base para Auditoría ---
class MovimientoCajaBaseSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar si la caja está abierta o cerrada
    caja_estado = serializers.BooleanField(source='caja.caja_estado', read_only=True)
    
    # Campo de solo lectura para mostrar el monto inicial de la caja
    caja_monto_inicial = serializers.DecimalField(source='caja.caja_monto_inicial', max_digits=10, decimal_places=2, read_only=True)

    # Validaciones: Aseguramos que la caja a la que se asocia el movimiento exista y esté abierta
    def validate_caja(self, value):
        try:
            caja = Caja.objects.get(pk=value.pk)
        except Caja.DoesNotExist:
            raise serializers.ValidationError("La caja especificada no existe.")
        
        # Validar si la caja está abierta
        if not caja.caja_estado:
            raise serializers.ValidationError("El movimiento no puede registrarse porque la caja está cerrada.")
        
        return value

    def create(self, validated_data):
        # Esta lógica se ejecuta al crear un movimiento y actualiza el saldo de la caja.
        caja = validated_data['caja']
        monto = validated_data['ingreso_monto'] if 'ingreso_monto' in validated_data else validated_data['egreso_monto']
        
        # Determine si es ingreso o egreso para aplicar la operación correcta
        es_ingreso = 'ingreso_monto' in validated_data

        # 1. Crear el objeto Ingreso/Egreso
        instance = super().create(validated_data)

        # 2. Actualizar el saldo final de la caja
        # Se asume que caja_saldo_final tiene el monto actual de la caja
        saldo_actual = caja.caja_saldo_final if caja.caja_saldo_final is not None else caja.caja_monto_inicial
        
        if es_ingreso:
            caja.caja_saldo_final = saldo_actual + monto
        else:
            # Es Egreso
            caja.caja_saldo_final = saldo_actual - monto
        
        caja.save(update_fields=['caja_saldo_final'])
        
        return instance


# --- Serializer para Egreso ---

class EgresoSerializer(MovimientoCajaBaseSerializer):
    class Meta:
        model = Egreso
        fields = ('id', 'caja', 'caja_estado', 'caja_monto_inicial', 'egreso_descripcion', 'egreso_monto', 'egreso_fecha_hora')
        read_only_fields = ('egreso_fecha_hora',)
        
    def validate(self, data):
        # Aquí forzamos la validación de la caja (si existe y está abierta)
        self.validate_caja(data['caja'])
        return data

# --- Serializer para Ingreso ---

class IngresoSerializer(MovimientoCajaBaseSerializer):
    class Meta:
        model = Ingreso
        fields = ('id', 'caja', 'caja_estado', 'caja_monto_inicial', 'ingreso_descripcion', 'ingreso_monto', 'ingreso_fecha_hora')
        read_only_fields = ('ingreso_fecha_hora',)
        
    def validate(self, data):
        # Aquí forzamos la validación de la caja (si existe y está abierta)
        self.validate_caja(data['caja'])
        return data
