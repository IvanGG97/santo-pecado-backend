from rest_framework import serializers
from .models import Pedido, Detalle_Pedido, Estado_Pedido
from inventario.models import Producto
from empleado.models import Empleado
from cliente.models import Cliente 
from cliente.serializers import ClienteSerializer

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
    # --- CAMBIO: Usar ClienteSerializer anidado ---
    # Esto incluirá todos los campos definidos en ClienteSerializer (nombre, direccion, etc.)
    # allow_null=True asegura que funcione si no hay cliente asociado
    cliente = ClienteSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Pedido
        # 'cliente' ya estaba en fields, pero ahora devolverá el objeto completo
        fields = ['id', 'cliente', 'empleado', 'estado_pedido', 'pedido_fecha_hora', 'detalles', 'total_pedido']

    def get_total_pedido(self, obj):
        return sum(item.cantidad * (item.precio_unitario or 0) for item in obj.detalles.all())
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
    # --- CAMPO CLIENTE AÑADIDO (Escritura) ---
    # Espera recibir el ID del cliente. Es opcional.
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), 
        required=False, # No es obligatorio asociar un cliente
        allow_null=True # Permite enviar null explícitamente
    )

    class Meta:
        model = Pedido
        # Añadir 'cliente' a la lista de fields
        fields = ['cliente', 'detalles'] 
        # Nota: 'empleado' y 'estado_pedido' se asignan automáticamente en el método create.
    
    def create(self, validated_data):
        # Verifica si el usuario tiene un perfil de empleado asociado
        if not hasattr(self.context['request'].user, 'empleado'):
            raise serializers.ValidationError("El usuario que realiza el pedido no tiene un perfil de empleado asociado.")
        
        empleado = self.context['request'].user.empleado
        
        # Busca el estado inicial (podrías hacerlo más robusto buscando por nombre si tienes varios)
        # Asegúrate de que exista al menos un estado en la BD.
        estado_inicial = Estado_Pedido.objects.order_by('id').first() 
        if not estado_inicial:
            raise serializers.ValidationError("No se encontró un estado inicial para el pedido. Por favor, cree uno en el panel de administrador.")

        detalles_data = validated_data.pop('detalles')
        
        # El campo 'cliente' (si vino en validated_data) se pasará automáticamente aquí
        pedido = Pedido.objects.create(
            empleado=empleado, 
            estado_pedido=estado_inicial, 
            **validated_data # Pasa 'cliente' y cualquier otro campo validado del Meta
        )

        # --- LÓGICA DE CREACIÓN DE DETALLES (sin cambios respecto a cliente) ---
        for detalle_data in detalles_data:
            producto_obj = detalle_data.get('producto') 
            notas_finales = detalle_data.get('notas', None) # Obtener notas, default None

            # Si las notas son None y es un producto (no promo), usamos el nombre del producto.
            if notas_finales is None and producto_obj:
                 notas_finales = producto_obj.producto_nombre
            # Si las notas son una cadena vacía, se guardará como vacía.

            Detalle_Pedido.objects.create(
                pedido=pedido,
                producto=producto_obj,
                cantidad=detalle_data['cantidad'],
                notas=notas_finales, # Guarda la nota procesada (puede ser nombre, personalización, o None/vacía)
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