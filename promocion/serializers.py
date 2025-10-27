from rest_framework import serializers
from .models import Promocion, Producto_Promocion
from inventario.models import Producto
# Importamos el serializer de Producto para la lógica de 'get_productos'
from inventario.serializers import ProductoSerializer 
import json

# --- Serializers para LEER (actualizados) ---

class ProductoEnPromocionReadSerializer(serializers.ModelSerializer):
    """ Muestra los detalles del producto dentro de una promoción. """
    class Meta:
        model = Producto
        fields = ['id', 'producto_nombre', 'producto_precio', 'producto_disponible']

class ProductoPromocionReadSerializer(serializers.ModelSerializer):
    producto = ProductoEnPromocionReadSerializer()
    class Meta:
        model = Producto_Promocion
        fields = ['producto', 'cantidad']

class PromocionReadSerializer(serializers.ModelSerializer):
    """ Serializer para LEER promociones con los detalles y cantidades de los productos. """
    productos_promocion = ProductoPromocionReadSerializer(many=True)
    promocion_disponible = serializers.SerializerMethodField()
    # 'promocion_imagen' ha sido eliminado
    promocion_imagen_url = serializers.CharField(read_only=True) # TextField se lee como CharField

    class Meta:
        model = Promocion
        fields = ('id', 'promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 
                  'promocion_fecha_hora_fin', 'promocion_stock', 'promocion_descripcion', 
                  'productos_promocion', 'promocion_disponible', 'promocion_estado',
                  'promocion_imagen_url') # 'promocion_imagen' eliminado

    def get_promocion_disponible(self, obj):
        if not obj.promocion_estado:
            return False
        for item in obj.productos_promocion.all():
            if not item.producto.producto_disponible:
                return False
        return True

# --- Serializers para ESCRIBIR (actualizados) ---

class ProductoPromocionWriteSerializer(serializers.Serializer):
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto')
    cantidad = serializers.IntegerField(min_value=1)

class PromocionWriteSerializer(serializers.ModelSerializer):
    productos = ProductoPromocionWriteSerializer(many=True, write_only=True)
    promocion_fecha_hora_inicio = serializers.DateTimeField(required=False, allow_null=True)
    promocion_fecha_hora_fin = serializers.DateTimeField(required=False, allow_null=True)
    promocion_imagen_url = serializers.CharField(required=False, allow_null=True)
    promocion_estado = serializers.BooleanField(required=False)

    class Meta:
        model = Promocion
        fields = ('promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 
                  'promocion_fecha_hora_fin', 'promocion_stock', 'promocion_descripcion', 
                  'productos', 'promocion_imagen_url', 'promocion_estado') # 'promocion_imagen' eliminado

    # El método 'to_internal_value' ya no es necesario,
    # porque el frontend solo enviará JSON.

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        # Lógica de imagen local eliminada
        promocion = Promocion.objects.create(**validated_data)
        for item_data in productos_data:
            Producto_Promocion.objects.create(promocion=promocion, **item_data)
        return promocion

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('productos', None)
        
        # Lógica de imagen local eliminada
        instance = super().update(instance, validated_data)
        
        if productos_data is not None:
            instance.productos_promocion.all().delete()
            for item_data in productos_data:
                Producto_Promocion.objects.create(promocion=instance, **item_data)
        
        return instance

