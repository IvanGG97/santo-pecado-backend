from rest_framework import generics, permissions
from .models import Venta, Estado_Venta
from .serializers import (
    VentaListSerializer, 
    VentaUpdateSerializer, 
    EstadoVentaSerializer
)

# --- Vista para LISTAR Ventas ---
class VentaListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar (GET) todas las ventas.
    """
    queryset = Venta.objects.all().select_related(
        'cliente', 
        'empleado__user', # Optimizar joins
        'caja', 
        'pedido', 
        'estado_venta'
    ).prefetch_related(
        'pedido__detalles__producto' # Optimizar prefetch
    ).order_by('-venta_fecha_hora') # Más nuevas primero
    
    serializer_class = VentaListSerializer
    permission_classes = [permissions.IsAuthenticated] # Ajustar permisos


# --- VISTA DE DETALLE (Para PATCH/PUT) ---
class VentaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para Ver (GET), Actualizar (PUT/PATCH) una venta específica.
    """
    queryset = Venta.objects.all()
    permission_classes = [permissions.IsAuthenticated] # Ajustar permisos
    
    # Devuelve el serializer correcto según la acción (Leer vs Escribir)
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VentaUpdateSerializer # Serializer de escritura (para guardar)
        return VentaListSerializer # Serializer de lectura (para ver)

# --- Vista para LISTAR Estados de Venta ---
class EstadoVentaListView(generics.ListAPIView):
    """
    Vista para obtener la lista de todos los posibles estados de venta.
    (Para los dropdowns en el frontend)
    """
    queryset = Estado_Venta.objects.all().order_by('id')
    serializer_class = EstadoVentaSerializer
    permission_classes = [permissions.IsAuthenticated]