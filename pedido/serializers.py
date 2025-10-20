from rest_framework import serializers
from .models import Pedido, Detalle_Pedido, Estado_Pedido
from inventario.models import Producto
from empleado.models import Empleado

# --- Serializers para LECTURA (mostrar datos) ---

class ProductoEnDetalleSerializer(serializers.ModelSerializer):
    """Serializer simple para mostrar el nombre del producto en un detalle."""
    class Meta:
        model = Producto
        fields = ['producto_nombre']

class DetallePedidoSerializer(serializers.ModelSerializer):
    """Serializer para mostrar los detalles de un pedido."""
    producto = ProductoEnDetalleSerializer(read_only=True)

    class Meta:
        model = Detalle_Pedido
        fields = ['producto', 'cantidad', 'precio_unitario']

class PedidoListSerializer(serializers.ModelSerializer):
    """Serializer para listar todos los pedidos."""
    empleado = serializers.StringRelatedField(source='empleado.user.username')
    estado_pedido = serializers.StringRelatedField()
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'empleado', 'estado_pedido', 'pedido_fecha_hora', 'detalles']

# --- Serializers para ESCRITURA (crear un nuevo pedido) ---

class DetallePedidoCreateSerializer(serializers.ModelSerializer):
    """Serializer para recibir los datos de un detalle al crear un pedido."""
    producto_id = serializers.IntegerField()

    class Meta:
        model = Detalle_Pedido
        fields = ['producto_id', 'cantidad']

class PedidoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear un nuevo pedido con sus detalles anidados.
    El empleado se asignará automáticamente desde el usuario autenticado.
    """
    detalles = DetallePedidoCreateSerializer(many=True)

    class Meta:
        model = Pedido
        # El estado inicial y el empleado no se piden, se asignan en la vista.
        fields = ['detalles']
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        # Creamos el objeto Pedido
        pedido = Pedido.objects.create(**validated_data)

        # Creamos los objetos Detalle_Pedido asociados
        for detalle_data in detalles_data:
            producto = Producto.objects.get(id=detalle_data['producto_id'])
            Detalle_Pedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=detalle_data['cantidad'],
                # Guardamos el precio del producto en el momento de la venta
                precio_unitario=producto.producto_precio 
            )
        return pedido

# --- Serializer para listar los estados de pedido ---
class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Pedido
        fields = '__all__'
