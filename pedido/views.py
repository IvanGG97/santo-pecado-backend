from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Pedido, Estado_Pedido
from .serializers import PedidoListSerializer, PedidoCreateSerializer, EstadoPedidoSerializer

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

    def perform_create(self, serializer):
        # Asigna automáticamente el empleado logueado y el estado inicial al crear.
        empleado = self.request.user.empleado
        # Asume que el primer estado es "Recibido" o similar. ¡Asegúrate de que exista!
        estado_inicial = Estado_Pedido.objects.first() 
        serializer.save(empleado=empleado, estado_pedido=estado_inicial)

class PedidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar (ej: cambiar estado) o eliminar un pedido específico.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoListSerializer
    permission_classes = [permissions.IsAuthenticated] # O IsAdminUser si solo admins pueden modificar

class EstadoPedidoListView(generics.ListAPIView):
    """
    Vista para listar todos los posibles estados de un pedido.
    """
    queryset = Estado_Pedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
