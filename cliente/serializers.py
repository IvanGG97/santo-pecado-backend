from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cliente.
    Se utiliza para la serialización y deserialización de objetos Cliente.
    """
    class Meta:
        model = Cliente
        # Incluye todos los campos del modelo Cliente
        fields = '__all__'
        # Los campos que deben ser leídos, pero no modificados directamente 
        # (aunque en este modelo no aplica, es buena práctica si tuvieras ids o fechas automáticas)
        read_only_fields = ('id',) 
