from rest_framework import serializers
from .models import Pedido, Detalle_Pedido, Estado_Pedido
from inventario.models import Producto
from empleado.models import Empleado
from cliente.models import Cliente 
from cliente.serializers import ClienteSerializer
from venta.models import Venta, Detalle_Venta, Estado_Venta

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
        # --- 1. OBTENER DATOS DEL PEDIDO ---
        if not hasattr(self.context['request'].user, 'empleado'):
            raise serializers.ValidationError("El usuario que realiza el pedido no tiene un perfil de empleado asociado.")
        
        empleado = self.context['request'].user.empleado
        estado_inicial_pedido = Estado_Pedido.objects.order_by('id').first() 
        if not estado_inicial_pedido:
            raise serializers.ValidationError("No se encontró un estado inicial para el Pedido.")

        detalles_data = validated_data.pop('detalles')
        cliente_obj = validated_data.pop('cliente', None) # Obtener el objeto Cliente (o None)

        # --- 2. CREAR PEDIDO Y DETALLES DE PEDIDO ---
        pedido = Pedido.objects.create(
            empleado=empleado, 
            estado_pedido=estado_inicial_pedido, 
            cliente=cliente_obj, # Asigna el cliente (o None)
            **validated_data
        )

        total_calculado = 0
        detalles_pedido_para_crear = []
        for detalle_data in detalles_data:
            producto_obj = detalle_data.get('producto')
            notas_finales = detalle_data.get('notas', None)

            if notas_finales is None and producto_obj:
                 notas_finales = producto_obj.producto_nombre
            
            # Calcular total
            total_calculado += (detalle_data['cantidad'] * detalle_data['precio_unitario'])

            detalles_pedido_para_crear.append(
                Detalle_Pedido(
                    pedido=pedido,
                    producto=producto_obj,
                    cantidad=detalle_data['cantidad'],
                    notas=notas_finales,
                    precio_unitario=detalle_data['precio_unitario']
                )
            )
        
        # Crear detalles de pedido en lote
        Detalle_Pedido.objects.bulk_create(detalles_pedido_para_crear)

        # --- 3. NUEVA LÓGICA: CREAR VENTA Y DETALLES DE VENTA ---
        try:
            # Obtener el estado inicial para la Venta (ej: "Pendiente" o "Pagada")
            # Asegúrate de tener al menos un Estado_Venta en tu BD
            estado_inicial_venta = Estado_Venta.objects.order_by('id').first()
            if not estado_inicial_venta:
                 # Si no hay estado de venta, solo loggea la advertencia pero no falles el pedido
                print("ADVERTENCIA: No se pudo crear la Venta. No se encontró un Estado_Venta inicial.")
                return pedido # Devuelve el pedido que sí se creó

            # Crear la Venta principal
            nueva_venta = Venta.objects.create(
                cliente=cliente_obj,        # Asigna el mismo cliente (o None)
                empleado=empleado,          # Asigna el mismo empleado
                caja=None,                  # Asigna None (asumiendo que hiciste el cambio en models.py)
                pedido=pedido,              # Vincula la venta al pedido
                estado_venta=estado_inicial_venta,
                venta_total=total_calculado, # Asigna el total calculado
                venta_medio_pago='efectivo',  # Asumimos 'efectivo' como default, ya que el pedido no incluye esta info
                venta_descuento=0           # Asumimos 0 descuento por ahora
            )

            # Copiar los detalles del pedido a los detalles de la venta
            detalles_venta_para_crear = []
            for detalle_data in detalles_data:
                # Solo añade detalles que sean productos reales (no el item de promo "padre")
                if detalle_data.get('producto'):
                    detalles_venta_para_crear.append(
                        Detalle_Venta(
                            venta=nueva_venta,
                            producto=detalle_data.get('producto'),
                            detalle_venta_cantidad=detalle_data['cantidad'],
                            detalle_venta_precio_unitario=detalle_data['precio_unitario'],
                            detalle_venta_descuento=0
                        )
                    )
            
            # Crear detalles de venta en lote
            Detalle_Venta.objects.bulk_create(detalles_venta_para_crear)

        except Exception as e:
            # Si la creación de la Venta falla (ej. por validación o error de BD),
            # no revertimos el Pedido (ya se creó). Solo informamos en la consola.
            print(f"ADVERTENCIA: El Pedido N°{pedido.id} se creó, pero la Venta automática falló: {e}")
        
        # --- FIN NUEVA LÓGICA ---

        return pedido # Devuelve el pedido original

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