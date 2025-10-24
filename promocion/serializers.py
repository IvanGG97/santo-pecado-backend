from rest_framework import serializers
from .models import Promocion, Producto_Promocion
from inventario.models import Producto

# --- Serializers para LEER (con campo de disponibilidad) ---

class ProductoEnPromocionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        # Incluimos el campo de disponibilidad del producto
        fields = ['id', 'producto_nombre', 'producto_precio', 'producto_disponible']

class ProductoPromocionReadSerializer(serializers.ModelSerializer):
    producto = ProductoEnPromocionReadSerializer()
    class Meta:
        model = Producto_Promocion
        fields = ['producto', 'cantidad']

class PromocionReadSerializer(serializers.ModelSerializer):
    productos_promocion = ProductoPromocionReadSerializer(many=True)
    # --- ¡NUEVO CAMPO CALCULADO! ---
    promocion_disponible = serializers.SerializerMethodField()

    class Meta:
        model = Promocion
        fields = ('id', 'promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 
                  'promocion_fecha_hora_fin', 'promocion_stock', 'promocion_descripcion', 
                  'productos_promocion', 'promocion_disponible') # <-- Añadido al final

    def get_promocion_disponible(self, obj):
        """
        Una promoción está disponible solo si todos sus productos lo están.
        """
        # Itera sobre cada producto dentro de la promoción
        for item in obj.productos_promocion.all():
            if not item.producto.producto_disponible:
                return False # Si encuentra un producto no disponible, la promoción entera no lo está
        return True # Si todos los productos están disponibles, la promoción lo está

# --- Serializers para ESCRIBIR (sin cambios) ---

class ProductoPromocionWriteSerializer(serializers.Serializer):
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto')
    cantidad = serializers.IntegerField(min_value=1)

class PromocionWriteSerializer(serializers.ModelSerializer):
    productos = ProductoPromocionWriteSerializer(many=True, write_only=True)
    promocion_fecha_hora_inicio = serializers.DateTimeField(required=False, allow_null=True)
    promocion_fecha_hora_fin = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Promocion
        fields = ('promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 
                  'promocion_fecha_hora_fin', 'promocion_stock', 'promocion_descripcion', 'productos')

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')
        promocion = Promocion.objects.create(**validated_data)
        for item_data in productos_data:
            Producto_Promocion.objects.create(promocion=promocion, **item_data)
        return promocion

    def update(self, instance, validated_data):
        productos_data = validated_data.pop('productos', None)
        instance = super().update(instance, validated_data)
        if productos_data is not None:
            instance.productos_promocion.all().delete()
            for item_data in productos_data:
                Producto_Promocion.objects.create(promocion=instance, **item_data)
        return instance

