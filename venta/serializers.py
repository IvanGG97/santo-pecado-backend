from rest_framework import serializers
from .models import Venta, Detalle_Venta, Estado_Venta
from pedido.models import Pedido, Detalle_Pedido # Importar Detalle_Pedido
from inventario.models import Producto
from cliente.serializers import ClienteSerializer
from empleado.serializers import EmpleadoSerializer # Importamos el EmpleadoSerializer existente

# --- Serializer para Listar Estados de Venta (Lectura) ---
class EstadoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Venta
        fields = ['id', 'estado_venta_nombre']

# --- Serializer para los Detalles del Pedido (con notas) ---
class DetallePedidoParaVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.producto_nombre', read_only=True, allow_null=True)
    producto_tipo = serializers.CharField(source='producto.tipo_producto.tipo_producto_nombre', read_only=True, allow_null=True)
    class Meta:
        model = Detalle_Pedido
        fields = ['id', 'producto_nombre', 'cantidad', 'precio_unitario', 'notas','producto_tipo'] # <-- Incluimos 'notas'


# --- Serializer para el Pedido (ACTUALIZADO) ---
class PedidoParaVentaSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoParaVentaSerializer(many=True, read_only=True)
    
    # --- CAMBIO AQUÍ: Añadir estado_pedido ---
    # Usamos StringRelatedField para obtener el nombre (ej: "En Preparación")
    estado_pedido = serializers.StringRelatedField(read_only=True)
    # --- FIN CAMBIO ---

    class Meta:
        model = Pedido
        # --- CAMBIO AQUÍ: Añadir 'estado_pedido' a fields ---
        fields = ['id', 'detalles', 'estado_pedido']


# --- Serializer para Listar Ventas (Lectura) ---
class VentaListSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True, allow_null=True)
    empleado = EmpleadoSerializer(source='empleado.user', read_only=True) 
    estado_venta = EstadoVentaSerializer(read_only=True) 
    pedido = PedidoParaVentaSerializer(read_only=True) # Este serializer ahora incluye el estado del pedido

    class Meta:
        model = Venta
        fields = [
            'id',
            'cliente',
            'empleado',
            'caja',
            'pedido', # <-- 'pedido' ahora contiene 'id', 'detalles' y 'estado_pedido'
            'estado_venta',
            'venta_fecha_hora',
            'venta_total',
            'venta_medio_pago',
            'venta_descuento',
        ]

# --- Serializer para Actualizar Venta (Escritura) ---
class VentaUpdateSerializer(serializers.ModelSerializer):
    estado_venta = serializers.PrimaryKeyRelatedField(queryset=Estado_Venta.objects.all())
    venta_medio_pago = serializers.ChoiceField(choices=Venta.MEDIO_PAGO_CHOICES)

    class Meta:
        model = Venta
        fields = ['estado_venta', 'venta_medio_pago']