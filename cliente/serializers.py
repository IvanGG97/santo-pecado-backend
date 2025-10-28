from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para leer y escribir datos del modelo Cliente.
    """
    class Meta:
        model = Cliente
        fields = [
            'id', 
            'cliente_dni', 
            'cliente_nombre', 
            'cliente_apellido', 
            'cliente_telefono', 
            'cliente_direccion', 
            'cliente_email'
        ]
        # Hacemos que DNI, apellido y email no sean requeridos a nivel de serializer,
        # ya que el modelo los permite como null/blank.
        extra_kwargs = {
            'cliente_dni': {'required': False, 'allow_null': True, 'allow_blank': True},
            'cliente_apellido': {'required': False, 'allow_null': True, 'allow_blank': True},
            'cliente_email': {'required': False, 'allow_null': True, 'allow_blank': True},
        }

    # Opcional: Validación para asegurar que al menos nombre o teléfono estén presentes si es necesario
    # def validate(self, data):
    #     if not data.get('cliente_nombre') and not data.get('cliente_telefono'):
    #         raise serializers.ValidationError("Debe proporcionar al menos un nombre o un teléfono.")
    #     return data
