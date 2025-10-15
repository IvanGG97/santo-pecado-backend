from rest_framework import generics, permissions
from .models import Venta, Estado_Venta
from .serializers import (
    VentaReadSerializer,
    VentaWriteSerializer,
    EstadoVentaSerializer
)

# --- Vistas para el modelo Venta ---

class VentaListCreateView(generics.ListCreateAPIView):
    """
    Vista de API para listar todas las ventas o crear una nueva venta.
    - GET: Devuelve una lista de todas las ventas.
    - POST: Crea una nueva venta junto con sus detalles.
    """
    queryset = Venta.objects.select_related(
        'cliente', 'empleado', 'caja', 'pedido', 'estado_venta'
    ).prefetch_related('detalle_venta_set__producto').all().order_by('-venta_fecha_hora')
    
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Determina qué serializador usar según el método de la petición.
        - Usa VentaReadSerializer para peticiones GET (lectura).
        - Usa VentaWriteSerializer para peticiones POST (escritura).
        """
        if self.request.method == 'POST':
            return VentaWriteSerializer
        return VentaReadSerializer

class VentaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista de API para ver, actualizar o eliminar una venta específica.
    - GET: Devuelve los detalles de una venta específica por su ID.
    - PUT/PATCH: Actualiza una venta.
    - DELETE: Elimina una venta.
    """
    queryset = Venta.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Usa el serializador de lectura para mostrar los datos.
        Para actualizar, se podría necesitar un serializador de escritura específico,
        pero por simplicidad, se puede reutilizar o adaptar según la necesidad.
        """
        # En una aplicación real, la lógica de actualización para datos anidados
        # puede requerir un VentaUpdateSerializer dedicado. Por ahora,
        # la lectura usará el ReadSerializer.
        return VentaReadSerializer


# --- Vistas para modelos relacionados ---

class EstadoVentaListView(generics.ListAPIView):
    """
    Vista de API para listar todos los estados de venta disponibles.
    Útil para llenar menús desplegables en el frontend.
    """
    queryset = Estado_Venta.objects.all()
    serializer_class = EstadoVentaSerializer
    permission_classes = [permissions.IsAuthenticated]
