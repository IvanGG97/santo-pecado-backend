from rest_framework import serializers
from .models import Estado_Pedido, Pedido, Detalle_Pedido
from inventario.models import Producto, Insumo, Producto_X_Insumo

class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Pedido
        fields = 'all'

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.producto_nombre', read_only=True)

    class Meta:
        model = Detalle_Pedido
        fields = ('id', 'producto', 'producto_nombre')
        # Puedes añadir campos como 'cantidad' aquí si los añades al modelo Detalle_Pedido

class PedidoSerializer(serializers.ModelSerializer):
# Campo anidado para recibir y mostrar los detalles del pedido
    detalles = DetallePedidoSerializer(source='detalle_pedido_set', many=True)

    # Campo de solo lectura para mostrar el nombre del estado
    estado_nombre = serializers.CharField(source='estado_pedido.estado_pedido_nombre', read_only=True)

    # Campo de solo lectura para el empleado (usando la relación inversa)
    empleado_nombre = serializers.CharField(source='empleado_x_rol.empleado.empleado_nombre', read_only=True)


    class Meta:
        model = Pedido
        fields = (
            'id', 
            'empleado_x_rol', 
            'empleado_nombre', 
            'estado_pedido', 
            'estado_nombre',
            'pedido_fecha_hora', 
            'detalles'
        )
        read_only_fields = ('pedido_fecha_hora',)

    # Método CREATE para manejar la creación anidada
    def create(self, validated_data):
        # 1. Separar los detalles (source='detalle_pedido_set' en la clase Meta)
        detalles_data = validated_data.pop('detalle_pedido_set')
        
        # 2. Crear el Pedido principal
        pedido = Pedido.objects.create(**validated_data)

        # 3. Crear los detalles del pedido
        for detalle_data in detalles_data:
            # Aquí asumimos que el detalle solo tiene 'producto' (ForeignKey) y 'cantidad'
            Detalle_Pedido.objects.create(pedido=pedido, **detalle_data)

            # TODO: Lógica de Stock y Recetas
            # Si el pedido está 'En Preparación' (Estado ID = 2) o 'Completado' (Estado ID = 3),
            # deberías iterar sobre la receta del producto y descontar los insumos del inventario.

        return pedido

    # Método UPDATE (necesario para manejar los detalles anidados)
    def update(self, instance, validated_data):
        # La lógica de UPDATE es más compleja ya que implica:
        # 1. Actualizar el pedido principal (ej. cambiar el estado)
        # 2. Crear nuevos detalles, modificar existentes o eliminar los que falten.
        
        # 1. Actualizar campos del Pedido principal (ej. estado)
        instance.empleado_x_rol = validated_data.get('empleado_x_rol', instance.empleado_x_rol)
        instance.estado_pedido = validated_data.get('estado_pedido', instance.estado_pedido)
        instance.save()
        
        # Si se envían detalles, se manejan aquí (omitido por simplicidad inicial en update)

        return instance