import logging

from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from .gemini import GeminiError, generar_reporte
from .models import Venta, Estado_Venta
from .serializers import (
    VentaListSerializer,
    VentaUpdateSerializer,
    EstadoVentaSerializer,
    ReporteIASerializer
)

logger = logging.getLogger(__name__)

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


# --- Permiso: los mismos roles que ven el dashboard en el frontend ---
class PuedeVerDashboard(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name__in=['Admin', 'Encargado/Cajero']).exists()
        )


# --- Vista para GENERAR el Reporte con IA ---
class ReporteIAView(APIView):
    """
    Vista para generar (POST) el reporte estratégico del dashboard con Gemini.
    La clave de la API queda solo en el servidor.
    """
    permission_classes = [PuedeVerDashboard]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'reporte_ia'

    def post(self, request):
        if not settings.GEMINI_API_KEY:
            return Response(
                {'detail': 'El reporte con IA no está configurado.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        serializer = ReporteIASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reporte = generar_reporte(serializer.validated_data)
        except GeminiError:
            logger.exception('No se pudo generar el reporte con Gemini')
            return Response(
                {'detail': 'No se pudo generar el reporte.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({'reporte': reporte})
