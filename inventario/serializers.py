from rest_framework import serializers
from .models import Producto, Tipo_Producto

# --- Serializers de Lectura (sin cambios) ---
class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Producto
        fields = ['id', 'tipo_producto_nombre']

class ProductoSerializer(serializers.ModelSerializer):
    tipo_producto = serializers.StringRelatedField()
    producto_imagen = serializers.ImageField(max_length=None, use_url=True, read_only=True)
    class Meta:
        model = Producto
        fields = [ 'id', 'producto_nombre', 'producto_descripcion', 'producto_precio', 'producto_disponible', 'producto_imagen', 'producto_imagen_url', 'tipo_producto' ]

# --- Serializer de Escritura (con lógica de eliminación de imagen) ---
class ProductoWriteSerializer(serializers.ModelSerializer):
    producto_imagen = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True)

    class Meta:
        model = Producto
        fields = [ 'tipo_producto', 'producto_nombre', 'producto_descripcion', 'producto_precio', 'producto_disponible', 'producto_imagen', 'producto_imagen_url' ]

    def to_internal_value(self, data):
        # ... (lógica de conversión de datos sin cambios) ...
        mutable_data = data.copy()
        for field_name in ['producto_imagen', 'producto_imagen_url', 'producto_descripcion']:
            if field_name in mutable_data and isinstance(mutable_data[field_name], str) and not mutable_data[field_name]:
                del mutable_data[field_name]
        disponible = mutable_data.get('producto_disponible')
        if isinstance(disponible, str):
            mutable_data['producto_disponible'] = disponible.lower() in ('true', 'on')
        tipo = mutable_data.get('tipo_producto')
        if isinstance(tipo, str) and tipo.isdigit():
            mutable_data['tipo_producto'] = int(tipo)
        return super().to_internal_value(mutable_data)

    def update(self, instance, validated_data):
        # --- LÓGICA PARA ELIMINAR LA IMAGEN ANTERIOR ---
        
        # Si se sube un nuevo archivo, borramos la imagen anterior (si existía)
        if 'producto_imagen' in validated_data:
            instance.producto_imagen.delete(save=False) # No guardar todavía
            instance.producto_imagen_url = None # Limpiamos la URL
        
        # Si se proporciona una nueva URL (y no un archivo), borramos la imagen anterior
        elif 'producto_imagen_url' in validated_data and validated_data['producto_imagen_url']:
            instance.producto_imagen.delete(save=False)

        # Si se envían los campos de imagen explícitamente como nulos, se borra la imagen
        if validated_data.get('producto_imagen') is None and validated_data.get('producto_imagen_url') is None:
             instance.producto_imagen.delete(save=False)
             instance.producto_imagen_url = None

        return super().update(instance, validated_data)

