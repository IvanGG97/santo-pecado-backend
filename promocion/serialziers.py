from rest_framework import serializers
from .models import Promocion, Producto_Promocion
from inventario.models import Producto
from inventario.serializers import ProductoSerializer # Asumiendo que este serializador existe

class ProductoPromocionWriteSerializer(serializers.ModelSerializer):
    """Serializador para escribir (crear/actualizar) la relación Producto-Promoción."""
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    class Meta:
        model = Producto_Promocion
        fields = ('producto',)

class PromocionSerializer(serializers.ModelSerializer):
    # Para la lectura (GET), mostramos los detalles completos del producto.
    # Usamos el related_name 'producto_promocion_set' que Django crea por defecto.
    # Usamos el related_name 'productos_promocion' que definiste en el modelo
    # y un serializador anidado para mostrar los detalles del producto.
    productos = ProductoPromocionWriteSerializer(many=True, read_only=True, source='productos_promocion')

    # Para la escritura (POST/PUT), esperamos una lista de IDs de productos.
    productos_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all()),
        write_only=True, source='productos_promocion'
    )

    class Meta:
        model = Promocion
        fields = ('id', 'promocion_nombre', 'promocion_precio', 'promocion_fecha_hora_inicio', 
                  'promocion_fecha_hora_fin', 'promocion_stock', 'promocion_descripcion', 
                  'productos', 'productos_ids')

    def create(self, validated_data):
        productos_data = validated_data.pop('productos_promocion')
        promocion = Promocion.objects.create(**validated_data)
        for producto_data in productos_data:
            Producto_Promocion.objects.create(promocion=promocion, producto=producto_data)
        return promocion

    def update(self, instance, validated_data):
        # El manejo de la actualización de relaciones anidadas puede ser complejo.
        # Una estrategia simple es borrar los existentes y crear los nuevos.
        productos_data = validated_data.pop('productos_promocion', None)
        
        # Actualiza los campos de la promoción
        instance = super().update(instance, validated_data)

        if productos_data is not None:
            # Borra las relaciones antiguas
            instance.productos_promocion.all().delete()
            # Crea las nuevas relaciones
            for producto_data in productos_data:
                Producto_Promocion.objects.create(promocion=instance, producto=producto_data)
        
        return instance
