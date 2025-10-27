from rest_framework import serializers
from .models import Pedido, Detalle_Pedido, Estado_Pedido
from inventario.models import Producto
from empleado.models import Empleado

# --- Serializers para LEER (mostrar datos) ---

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.producto_nombre', read_only=True)
    class Meta:
        model = Detalle_Pedido
        fields = ['producto_nombre', 'cantidad', 'precio_unitario', 'notas']

class PedidoListSerializer(serializers.ModelSerializer):
    empleado = serializers.StringRelatedField(source='empleado.user.username')
    estado_pedido = serializers.StringRelatedField()
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    total_pedido = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'empleado', 'estado_pedido', 'pedido_fecha_hora', 'detalles', 'total_pedido']

    def get_total_pedido(self, obj):
        return sum(item.cantidad * item.precio_unitario for item in obj.detalles.all())

# --- Serializers para ESCRIBIR (crear un nuevo pedido) ---

class DetallePedidoCreateSerializer(serializers.Serializer):
    """
    Valida los datos de CADA item que viene en un nuevo pedido.
    """
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', required=False, allow_null=True)
    cantidad = serializers.IntegerField(min_value=1)
    notas = serializers.CharField(required=False, allow_blank=True) # Permitir explícitamente que esté en blanco
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2) # Acepta el precio del frontend

class PedidoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer principal para crear un Pedido con todos sus detalles.
    """
    detalles = DetallePedidoCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Pedido
        fields = ['detalles']
    
    def create(self, validated_data):
        if not hasattr(self.context['request'].user, 'empleado'):
            raise serializers.ValidationError("El usuario que realiza el pedido no tiene un perfil de empleado asociado.")
        
        empleado = self.context['request'].user.empleado
        estado_inicial = Estado_Pedido.objects.first()
        if not estado_inicial:
            raise serializers.ValidationError("No se encontró un estado inicial para el pedido. Por favor, cree uno en el panel de administrador.")

        detalles_data = validated_data.pop('detalles')
        
        pedido = Pedido.objects.create(
            empleado=empleado, 
            estado_pedido=estado_inicial, 
            **validated_data
        )

        # --- LÓGICA DE CREACIÓN DE DETALLES CORREGIDA ---
        for detalle_data in detalles_data:
            producto_obj = detalle_data.get('producto')
            notas_finales = detalle_data.get('notas', '')

            # Si las notas están vacías y es un producto, usamos el nombre del producto.
            if not notas_finales and producto_obj:
                notas_finales = producto_obj.producto_nombre

            Detalle_Pedido.objects.create(
                pedido=pedido,
                producto=producto_obj,
                cantidad=detalle_data['cantidad'],
                notas=notas_finales,
                precio_unitario=detalle_data['precio_unitario'] # ¡USA EL PRECIO DEL FRONTEND!
            )
        return pedido

# --- Serializer para listar los estados de pedido ---
class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Pedido
        fields = ['id', 'estado_pedido_nombre']

class PedidoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para actualizar solo el estado de un pedido.
    Espera recibir el ID del nuevo Estado_Pedido.
    """
    # Hacemos explícito que esperamos un ID para el ForeignKey
    estado_pedido = serializers.PrimaryKeyRelatedField(queryset=Estado_Pedido.objects.all())

    class Meta:
        model = Pedido
        fields = ['estado_pedido'] # Solo permite actualizar este campo