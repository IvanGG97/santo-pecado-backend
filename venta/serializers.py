from rest_framework import serializers
from .models import Venta, Detalle_Venta, Estado_Venta
from cliente.models import Cliente
from empleado.models import Empleado
from caja.models import Caja
from inventario.models import Producto

# --- Serializers Simples ---

class EstadoVentaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Estado_Venta.
    """
    class Meta:
        model = Estado_Venta
        fields = '__all__'


# --- Serializers de Lectura (Para GET requests) ---
# Estos serializers están optimizados para mostrar la información de una
# forma clara y legible, anidando detalles y mostrando nombres en lugar de IDs.

class DetalleVentaReadSerializer(serializers.ModelSerializer):
    """
    Muestra los detalles de una venta, incluyendo el nombre del producto.
    """
    # Suponiendo que el modelo Producto tiene un campo 'producto_nombre'.
    producto_nombre = serializers.CharField(source='producto.producto_nombre', read_only=True)

    class Meta:
        model = Detalle_Venta
        fields = [
            'id', 
            'producto', 
            'producto_nombre', 
            'detalle_venta_cantidad', 
            'detalle_venta_precio_unitario', 
            'detalle_venta_descuento'
        ]

class VentaReadSerializer(serializers.ModelSerializer):
    """
    Muestra una venta con toda su información relacionada de forma detallada.
    """
    # Usamos StringRelatedField para mostrar el __str__ del modelo relacionado.
    cliente = serializers.StringRelatedField()
    empleado = serializers.StringRelatedField()
    caja = serializers.StringRelatedField()
    pedido = serializers.StringRelatedField()
    estado_venta = serializers.StringRelatedField()

    # Anidamos los detalles de la venta usando el serializer de lectura.
    # 'detalle_venta_set' es el related_name por defecto que Django crea.
    detalles = DetalleVentaReadSerializer(source='detalle_venta_set', many=True, read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'empleado', 'caja', 'pedido', 'estado_venta', 
            'venta_fecha_hora', 'venta_total', 'venta_medio_pago', 
            'venta_descuento', 'detalles'
        ]


# --- Serializers de Escritura (Para POST/PUT requests) ---
# Estos serializers están diseñados para recibir datos y crear nuevos
# objetos en la base de datos, manejando la creación anidada de detalles.

class DetalleVentaWriteSerializer(serializers.ModelSerializer):
    """
    Define los campos que se esperan para cada detalle al crear una venta.
    """
    class Meta:
        model = Detalle_Venta
        # El campo 'venta' se asignará automáticamente en la lógica de creación.
        fields = [
            'producto', 
            'detalle_venta_cantidad', 
            'detalle_venta_precio_unitario', 
            'detalle_venta_descuento'
        ]

class VentaWriteSerializer(serializers.ModelSerializer):
    """
    Permite crear una Venta y sus Detalles en una sola petición POST.
    """
    # Campo para recibir la lista de detalles de la venta.
    # 'write_only=True' significa que este campo se usa para crear/actualizar,
    # pero no se mostrará al leer una venta.
    detalles = DetalleVentaWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Venta
        fields = [
            'cliente', 'empleado', 'caja', 'pedido', 'estado_venta',
            'venta_total', 'venta_medio_pago', 'venta_descuento', 'detalles'
        ]

    def create(self, validated_data):
        """
        Sobrescribimos el método create para manejar la creación anidada.
        """
        # 1. Extraemos los datos de los detalles del diccionario validado.
        detalles_data = validated_data.pop('detalles')
        
        # 2. Creamos el objeto Venta principal con el resto de los datos.
        venta = Venta.objects.create(**validated_data)
        
        # 3. Iteramos sobre los datos de los detalles y creamos cada objeto Detalle_Venta,
        #    asociándolo a la Venta que acabamos de crear.
        for detalle_data in detalles_data:
            Detalle_Venta.objects.create(venta=venta, **detalle_data)
            
        return venta
