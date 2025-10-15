from rest_framework import viewsets, permissions
from .models import Proveedor, Compra, Detalle_Compra
from .serializers import ProveedorSerializer, CompraSerializer, DetalleCompraSerializer

# --- ViewSet para Proveedor (CRUD simple) ---
class ProveedorViewSet(viewsets.ModelViewSet):
    """Permite listar, crear, recuperar, actualizar y eliminar proveedores."""
    # Ordenamos por nombre para que la lista sea fácil de navegar
    queryset = Proveedor.objects.all().order_by('proveedor_nombre')
    serializer_class = ProveedorSerializer
    # Solo usuarios autenticados (empleados) pueden gestionar proveedores
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['proveedor_nombre', 'proveedor_dni']

# --- ViewSet para Compra (CRUD complejo con lógica de negocio) ---
class CompraViewSet(viewsets.ModelViewSet):
    """Permite listar, crear, recuperar, actualizar y eliminar compras,
    incluyendo la lógica para el total y actualización de stock en la creación.
    """
    # Usamos select_related para optimizar la consulta y obtener datos relacionados
    queryset = Compra.objects.all().select_related('proveedor', 'empleado', 'caja').order_by('-compra_fecha_hora')
    serializer_class = CompraSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Filtros por los que se puede buscar rápidamente
    filterset_fields = ['proveedor', 'empleado', 'caja', 'compra_metodo_pago']
    search_fields = ['proveedor__proveedor_nombre', 'empleado__empleado_nombre']
    
# --- ViewSet para Detalle_Compra (Solo para referencia) ---
class DetalleCompraViewSet(viewsets.ModelViewSet):
    """Permite listar y ver detalles de las líneas de compra."""
    queryset = Detalle_Compra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]
