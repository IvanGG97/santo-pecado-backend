from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError # <-- 1. Importar ValidationError
from .models import Pedido, Estado_Pedido
from .serializers import (
    PedidoListSerializer, 
    PedidoCreateSerializer, 
    EstadoPedidoSerializer,
    PedidoUpdateSerializer # Importar el serializer de actualización
)

class PedidoListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todos los pedidos (GET) o crear un nuevo pedido (POST).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optimizar la consulta para incluir datos relacionados
        return Pedido.objects.all().select_related(
            'cliente', 'empleado__user', 'estado_pedido'
        ).prefetch_related(
            'detalles__producto' # Precargar detalles y productos
        ).order_by('-pedido_fecha_hora')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PedidoCreateSerializer
        return PedidoListSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class PedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar (ej: cambiar estado) o eliminar un pedido específico.
    """
    queryset = Pedido.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # Usar el serializer correcto según la acción
        if self.request.method in ['PUT', 'PATCH']:
            return PedidoUpdateSerializer # Serializer de escritura para actualizar
        return PedidoListSerializer # Serializer de lectura para GET

    # --- 2. AÑADIR ESTE MÉTODO COMPLETO ---
    def partial_update(self, request, *args, **kwargs):
        """
        Sobrescribe el método PATCH (actualización parcial) para capturar
        los ValidationErrors que provienen de la señal de stock.
        """
        try:
            # Intenta ejecutar la lógica de actualización normal (que llama a save() y dispara la señal)
            return super().partial_update(request, *args, **kwargs)
        
        except ValidationError as e:
            # --- 3. CAPTURAR EL ERROR DE STOCK ---
            # Si la señal (pedido/signals.py) levanta un ValidationError,
            # lo capturamos aquí.
            
            # Extraemos el mensaje de error específico (ej. "El insumo 'Tomate' es insuficiente...")
            error_message = e.message if hasattr(e, 'message') else e.messages[0]
            
            # Devolvemos una respuesta 400 Bad Request con el mensaje
            # que el frontend SÍ puede leer desde (err.response.data.detail)
            return Response(
                {"detail": error_message}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Capturar cualquier otro error inesperado
            return Response(
                {"detail": f"Ocurrió un error inesperado en el servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    # --- FIN DEL MÉTODO AÑADIDO ---


class EstadoPedidoListView(generics.ListAPIView):
    """
    Vista para listar todos los posibles estados de un pedido.
    """
    queryset = Estado_Pedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [permissions.IsAuthenticated]