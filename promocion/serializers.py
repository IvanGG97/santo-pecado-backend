from rest_framework import serializers
from .models import Promocion, Producto_Promocion
from inventario.models import Producto

# --- Serializers para LEER (sin cambios) ---
class ProductoEnPromocionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'producto_nombre', 'producto_precio']

class ProductoPromocionReadSerializer(serializers.ModelSerializer):
    producto = ProductoEnPromocionReadSerializer()
    class Meta:
        model = Producto_Promocion
        fields = ['producto', 'cantidad']

class PromocionReadSerializer(serializers.ModelSerializer):
    productos_promocion = ProductoPromocionReadSerializer(many=True)
    class Meta:
        model = Promocion
        fields = ('id', 'promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 
                  'promocion_fecha_hora_fin', 'promocion_stock', 'promocion_descripcion', 'productos_promocion')

# --- Serializers para ESCRIBIR (con la solución para las fechas) ---
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

    # --- MÉTODO AÑADIDO PARA LA SOLUCIÓN ---
    def to_internal_value(self, data):
        """
        Limpia los campos de fecha si vienen como strings vacíos.
        """
        mutable_data = data.copy()
        
        # Si el campo de fecha de inicio es un string vacío, lo convertimos a None
        inicio = mutable_data.get('promocion_fecha_hora_inicio')
        if isinstance(inicio, str) and not inicio:
            mutable_data['promocion_fecha_hora_inicio'] = None

        # Hacemos lo mismo para la fecha de fin
        fin = mutable_data.get('promocion_fecha_hora_fin')
        if isinstance(fin, str) and not fin:
            mutable_data['promocion_fecha_hora_fin'] = None
            
        return super().to_internal_value(mutable_data)
    # ----------------------------------------

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

