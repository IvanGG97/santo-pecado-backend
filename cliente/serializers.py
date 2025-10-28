from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id', # Incluir id es útil para el frontend
            'cliente_dni',
            'cliente_nombre',
            'cliente_apellido',
            'cliente_telefono',
            'cliente_direccion',
            'cliente_email'
        ]
        # Asegura que los campos opcionales en el modelo lo sean en la API
        extra_kwargs = {
            'cliente_dni': {'required': False, 'allow_blank': True, 'allow_null': True},
            'cliente_apellido': {'required': False, 'allow_blank': True, 'allow_null': True},
            'cliente_email': {'required': False, 'allow_blank': True, 'allow_null': True},
            # Dirección no necesita required=False porque no tiene null=True o blank=True en el modelo original que me pasaste,
            # pero si lo hiciste opcional, añádelo aquí también.
            # 'cliente_direccion': {'required': False, 'allow_blank': True, 'allow_null': True}, # Si aplica
        }

    # --- NUEVO: Convertir DNI vacío a None ---
    def to_internal_value(self, data):
        # Llama primero al método original para obtener los datos validados
        internal_value = super().to_internal_value(data)

        # Si 'cliente_dni' está presente y es una cadena vacía, conviértelo a None
        if 'cliente_dni' in internal_value and internal_value['cliente_dni'] == '':
            internal_value['cliente_dni'] = None

        # Haz lo mismo para otros campos unique que permitan null/blank si los tienes
        # if 'cliente_email' in internal_value and internal_value['cliente_email'] == '':
        #     internal_value['cliente_email'] = None

        return internal_value
    # --- FIN NUEVO ---