from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import Pedido, Detalle_Pedido, Estado_Pedido
# Se necesitarán los serializers que aún no hemos creado
# from .serializers import PedidoSerializer, DetallePedidoSerializer, EstadoPedidoSerializer 


# ViewSet de solo lectura para los estados de pedido (catálogo)
class EstadoPedidoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Permite ver los estados disponibles de un pedido (Ej: 'Pendiente', 'En Preparación', 'Entregado').
    """
    queryset = Estado_Pedido.objects.all()
    # serializer_class = EstadoPedidoSerializer # Necesita el serializer correspondiente
    permission_classes = [permissions.IsAuthenticated]


# ViewSet principal para la gestión de Pedidos
class PedidoViewSet(viewsets.ModelViewSet):
    """
    Permite CRUD completo sobre pedidos. La creación del pedido incluye detalles anidados.
    """
    # Consulta optimizada para cargar los detalles del pedido y los productos relacionados
    queryset = Pedido.objects.select_related(
        'estado_pedido', 
        'empleado_x_rol__empleado'
    ).prefetch_related(
        Prefetch(
            'detalle_pedido_set', 
            queryset=Detalle_Pedido.objects.select_related('producto')
        )
    ).all().order_by('-pedido_fecha_hora')
    
    # serializer_class = PedidoSerializer # Necesita el serializer correspondiente
    permission_classes = [permissions.IsAuthenticated]

    # --- Acciones Personalizadas de Negocio ---

    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        """
        Endpoint para cambiar el estado de un pedido específico.
        Requiere enviar el nuevo ID de estado en el cuerpo de la petición: {"estado_id": 3}
        """
        pedido = self.get_object()
        nuevo_estado_id = request.data.get('estado_id')
        
        if not nuevo_estado_id:
            return Response({'error': 'Debe proporcionar el ID del nuevo estado (estado_id).'}, status=400)
        
        try:
            nuevo_estado = Estado_Pedido.objects.get(pk=nuevo_estado_id)
            pedido.estado_pedido = nuevo_estado
            pedido.save()
            # Retornamos el serializer actualizado.
            # return Response(self.get_serializer(pedido).data) # Necesita el serializer
            return Response({'status': f'Estado de pedido N°{pk} actualizado a {nuevo_estado.estado_pedido_nombre}'})

        except Estado_Pedido.DoesNotExist:
            return Response({'error': f'El estado con ID {nuevo_estado_id} no existe.'}, status=404)
