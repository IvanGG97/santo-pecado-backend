from rest_framework import serializers
from .models import Pedido, Detalle_Pedido, Estado_Pedido
from inventario.models import Producto
from empleado.models import Empleado
from cliente.models import Cliente 
from cliente.serializers import ClienteSerializer
from venta.models import Venta, Detalle_Venta, Estado_Venta
from caja.models import Caja # <--- 1. IMPORTAR CAJA

# --- Serializers para LEER (mostrar datos) ---

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.producto_nombre', read_only=True, allow_null=True)
    class Meta:
        model = Detalle_Pedido
        fields = ['producto_nombre', 'cantidad', 'precio_unitario', 'notas']

class PedidoListSerializer(serializers.ModelSerializer):
    empleado = serializers.StringRelatedField(source='empleado.user.username')
    estado_pedido = serializers.StringRelatedField()
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    total_pedido = serializers.SerializerMethodField()
    cliente = ClienteSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'empleado', 'estado_pedido', 'pedido_fecha_hora', 'detalles', 'total_pedido']

    def get_total_pedido(self, obj):
        return sum(item.cantidad * (item.precio_unitario or 0) for item in obj.detalles.all())

# --- Serializers para ESCRIBIR (crear un nuevo pedido) ---

class DetallePedidoCreateSerializer(serializers.Serializer):
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', required=False, allow_null=True)
    cantidad = serializers.IntegerField(min_value=1)
    notas = serializers.CharField(required=False, allow_blank=True, allow_null=True) # Permitir null
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)

class PedidoCreateSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoCreateSerializer(many=True, write_only=True)
    cliente = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), 
        required=False,
        allow_null=True
    )

    class Meta:
        model = Pedido
        fields = ['cliente', 'detalles'] 
    
    def create(self, validated_data):
        # --- 1. OBTENER DATOS DEL PEDIDO ---
        if not hasattr(self.context['request'].user, 'empleado'):
            raise serializers.ValidationError("El usuario que realiza el pedido no tiene un perfil de empleado asociado.")
        
        empleado = self.context['request'].user.empleado
        estado_inicial_pedido = Estado_Pedido.objects.order_by('id').first() 
        if not estado_inicial_pedido:
            raise serializers.ValidationError("No se encontró un estado inicial para el Pedido.")

        # --- CORRECCIÓN: Usar .pop() para extraer cliente ---
        detalles_data = validated_data.pop('detalles')
        cliente_obj = validated_data.pop('cliente', None) # Extrae el cliente (o None)

        # --- 2. CREAR PEDIDO Y DETALLES DE PEDIDO ---
        pedido = Pedido.objects.create(
            empleado=empleado, 
            estado_pedido=estado_inicial_pedido, 
            cliente=cliente_obj, 
            **validated_data # validated_data ya no tiene 'cliente'
        )

        total_calculado = 0
        detalles_pedido_para_crear = []
        for detalle_data in detalles_data:
            producto_obj = detalle_data.get('producto')
            notas_finales = detalle_data.get('notas', None)

            if notas_finales is None and producto_obj:
                 notas_finales = producto_obj.producto_nombre
            
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
        
        Detalle_Pedido.objects.bulk_create(detalles_pedido_para_crear)

        # --- 3. LÓGICA DE VENTA (ACTUALIZADA) ---
        try:
            # --- CORRECCIÓN: Buscar la caja abierta ---
            try:
                caja_abierta = Caja.objects.get(caja_estado=True)
            except Caja.DoesNotExist:
                raise serializers.ValidationError("No se encontró una caja abierta. No se puede registrar la venta.")
            except Caja.MultipleObjectsReturned:
                raise serializers.ValidationError("Error: Hay múltiples cajas abiertas. Cierre la caja anterior.")
            # --- FIN CORRECCIÓN ---

            estado_inicial_venta = Estado_Venta.objects.get(estado_venta_nombre="No Pagado") # Asumimos estado "No Pagado"
            if not estado_inicial_venta:
                print("ADVERTENCIA: No se pudo crear la Venta. No se encontró el Estado_Venta 'No Pagado'.")
                return pedido 

            nueva_venta = Venta.objects.create(
                cliente=cliente_obj,
                empleado=empleado,
                caja=caja_abierta,              # <-- CORREGIDO (antes era None)
                pedido=pedido,
                estado_venta=estado_inicial_venta,
                venta_total=total_calculado,
                venta_medio_pago='efectivo', # Default (se cambia en VentasPage)
                venta_descuento=0
            )

            detalles_venta_para_crear = []
            for detalle_data in detalles_data:
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
            
            Detalle_Venta.objects.bulk_create(detalles_venta_para_crear)

        except Exception as e:
            print(f"ADVERTENCIA: El Pedido N°{pedido.id} se creó, pero la Venta automática falló: {e}")
        
        return pedido

# --- Serializer para listar los estados de pedido ---
class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Pedido
        fields = ['id', 'estado_pedido_nombre']

# --- Serializer para actualizar estado de pedido (CocinaPage) ---
class PedidoUpdateSerializer(serializers.ModelSerializer):
    estado_pedido = serializers.PrimaryKeyRelatedField(queryset=Estado_Pedido.objects.all())

    class Meta:
        model = Pedido
        fields = ['estado_pedido']