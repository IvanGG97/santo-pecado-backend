from rest_framework import viewsets, permissions
from .models import Egreso, Ingreso
from .serializers import EgresoSerializer, IngresoSerializer # Necesitarás crear este archivo

# --- ViewSets para Egresos ---

class EgresoViewSet(viewsets.ModelViewSet):
    """
    Permite listar, crear y gestionar Egresos.
    El Egreso representa una salida de dinero de una caja.
    """
    queryset = Egreso.objects.all().select_related('caja').order_by('-egreso_fecha_hora')
    serializer_class = EgresoSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo empleados autenticados pueden crear egresos
    search_fields = ['egreso_descripcion', 'caja__id']
    filterset_fields = ['caja', 'egreso_fecha_hora']


# --- ViewSets para Ingresos ---

class IngresoViewSet(viewsets.ModelViewSet):
    """
    Permite listar, crear y gestionar Ingresos.
    El Ingreso representa una entrada de dinero a una caja (no proveniente de una venta).
    """
    queryset = Ingreso.objects.all().select_related('caja').order_by('-ingreso_fecha_hora')
    serializer_class = IngresoSerializer
    permission_classes = [permissions.IsAuthenticated] # Solo empleados autenticados pueden crear ingresos
    search_fields = ['ingreso_descripcion', 'caja__id']
    filterset_fields = ['caja', 'ingreso_fecha_hora']
