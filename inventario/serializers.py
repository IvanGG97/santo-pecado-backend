from rest_framework import serializers
from .models import (
    Tipo_Producto, 
    Categoria_Insumo, 
    Producto, 
    Insumo, 
    Producto_X_Insumo
)

# Serializer para Modelos Simples
class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Producto
        fields = '__all__'

class CategoriaInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria_Insumo
        fields = '__all__'


# Serializer para Insumo
class InsumoSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre de la categoría del insumo
    categoria_nombre = serializers.CharField(source='categoria_insumo.categoria_insumo_nombre', read_only=True)
    
    class Meta:
        model = Insumo
        fields = '__all__'
        read_only_fields = ('insumo_stock',) # El stock se maneja por movimientos, no se edita directamente

# --- Serializers Anidados para "Recetas" ---

class ProductoXInsumoSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para el nombre del Insumo, útil para la respuesta GET
    insumo_nombre = serializers.CharField(source='insumo.insumo_nombre', read_only=True)
    insumo_unidad = serializers.CharField(source='insumo.insumo_unidad', read_only=True)

    class Meta:
        model = Producto_X_Insumo
        # Solo pedimos el ID del insumo y la cantidad
        fields = ('id', 'insumo', 'insumo_nombre', 'insumo_unidad', 'producto_insumo_cantidad')
        read_only_fields = ('id',)


class ProductoSerializer(serializers.ModelSerializer):
    # 1. Serializer Anidado para las "Recetas" (relación inversa: producto_x_insumo_set)
    recetas = ProductoXInsumoSerializer(source='producto_x_insumo_set', many=True, required=False)
    
    # 2. Campos de Solo Lectura para nombres (mejor presentación en GET)
    tipo_producto_nombre = serializers.CharField(source='tipo_producto.tipo_producto_nombre', read_only=True)

    class Meta:
        model = Producto
        fields = (
            'id', 'tipo_producto', 'tipo_producto_nombre', 'producto_nombre', 
            'producto_descripcion', 'producto_precio', 'producto_disponible', 
            'producto_imagen', 'producto_fecha_hora_creacion', 'recetas'
        )
        read_only_fields = ('producto_fecha_hora_creacion',)

    def create(self, validated_data):
        # Maneja la creación de Producto y sus recetas anidadas
        recetas_data = validated_data.pop('producto_x_insumo_set', [])
        producto = Producto.objects.create(**validated_data)
        
        for receta_data in recetas_data:
            Producto_X_Insumo.objects.create(producto=producto, **receta_data)
        
        return producto

    def update(self, instance, validated_data):
        # Maneja la actualización de Producto y la edición de sus recetas
        recetas_data = validated_data.pop('producto_x_insumo_set', None)
        
        # 1. Actualizar campos del Producto
        instance = super().update(instance, validated_data)
        
        # 2. Gestionar las Recetas (si se enviaron)
        if recetas_data is not None:
            instance.producto_x_insumo_set.all().delete() # Estrategia simple: borrar y recrear
            for receta_data in recetas_data:
                Producto_X_Insumo.objects.create(producto=instance, **receta_data)
        
        return instance
