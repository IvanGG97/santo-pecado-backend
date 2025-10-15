from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from .models import Proveedor, Compra, Detalle_Compra
from inventario.models import Insumo

# Nota: Asumo que tienes un modelo Caja importable, aunque no se usa en este archivo, lo dejo para futuras integraciones.
# from caja.models import Caja 

# --- Serializer para Detalle_Compra (Anidado) ---
class DetalleCompraSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para el nombre del insumo (mejora la lectura)
    insumo_nombre = serializers.CharField(source='insumo.insumo_nombre', read_only=True)

    class Meta:
        model = Detalle_Compra
        fields = (
            'insumo', 
            'insumo_nombre', 
            'detalle_compra_cantidad', 
            'detalle_compra_precio_unitario'
        )

# --- Serializer para Proveedor ---
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

# --- Serializer para Compra (Principal) ---
class CompraSerializer(serializers.ModelSerializer):
    # Serializer anidado: permite crear o leer los detalles en el mismo objeto Compra
    detalles = DetalleCompraSerializer(many=True) 
    
    # Campos de solo lectura para las relaciones
    proveedor_nombre = serializers.CharField(source='proveedor.proveedor_nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado.empleado_nombre', read_only=True)
    
    class Meta:
        model = Compra
        fields = '__all__'
        read_only_fields = ('compra_fecha_hora', 'compra_total')

    def create(self, validated_data):
        # Usamos una transacción para asegurar que todo se complete o se revierta
        with transaction.atomic():
            detalles_data = validated_data.pop('detalles')
            
            # 1. Calcular el Total de la Compra
            compra_total = sum(
                item['detalle_compra_cantidad'] * item['detalle_compra_precio_unitario']
                for item in detalles_data
            )
            validated_data['compra_total'] = compra_total

            # 2. Crear el objeto Compra
            compra = Compra.objects.create(**validated_data)

            # 3. Procesar cada detalle y actualizar stock
            for detalle_data in detalles_data:
                insumo = detalle_data.pop('insumo')
                cantidad_comprada = detalle_data['detalle_compra_cantidad']

                # Crear el Detalle_Compra
                Detalle_Compra.objects.create(compra=compra, insumo=insumo, **detalle_data)
                
                # 4. Actualizar el stock del insumo y el precio de compra usando F()
                Insumo.objects.filter(pk=insumo.pk).update(
                    insumo_stock=F('insumo_stock') + cantidad_comprada,
                    insumo_precio_compra=detalle_data['detalle_compra_precio_unitario']
                )

            # TODO: Lógica de Caja: Si la compra es 'efectivo', debes registrar un Egreso 
            # en la app movimiento_caja y actualizar el saldo de la Caja.
            
            return compra