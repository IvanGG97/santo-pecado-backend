from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Pedido, Estado_Pedido
from .serializers import PedidoListSerializer, PedidoCreateSerializer, EstadoPedidoSerializer,PedidoUpdateSerializer

class PedidoListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar todos los pedidos (GET) o crear un nuevo pedido (POST).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Devuelve todos los pedidos, el más reciente primero.
        return Pedido.objects.all().order_by('-pedido_fecha_hora')

    def get_serializer_class(self):
        # Usa un serializer diferente para leer (GET) y para crear (POST)
        if self.request.method == 'POST':
            return PedidoCreateSerializer
        return PedidoListSerializer

    def get_serializer_context(self):
        """
        Pasa el 'request' completo al contexto del serializer.
        Esto es crucial para que PedidoCreateSerializer pueda acceder a request.user.
        """
        return {'request': self.request}

class PedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar (ej: cambiar estado) o eliminar un pedido específico.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoListSerializer # Usa el serializer de lectura para ver el detalle
    permission_classes = [permissions.IsAuthenticated] # O IsAdminUser si solo admins pueden modificar

class EstadoPedidoListView(generics.ListAPIView):
    """
    Vista para listar todos los posibles estados de un pedido.
    """
    queryset = Estado_Pedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar (ej: cambiar estado) o eliminar un pedido específico.
    """
    queryset = Pedido.objects.all()
    permission_classes = [permissions.IsAuthenticated] # O IsAdminUser si solo admins pueden modificar

    # --- MÉTODO get_serializer_class AÑADIDO ---
    def get_serializer_class(self):
        """
        Usa PedidoUpdateSerializer para PUT/PATCH, y PedidoListSerializer para GET.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return PedidoUpdateSerializer
        return PedidoListSerializer # Serializer por defecto para GET