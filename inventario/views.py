from rest_framework import viewsets, permissions
from .models import (
    Tipo_Producto, 
    Categoria_Insumo, 
    Producto, 
    Insumo, 
    Producto_X_Insumo
)
from .serializers import (
    TipoProductoSerializer,
    CategoriaInsumoSerializer,
    ProductoSerializer,
    InsumoSerializer,
    ProductoXInsumoSerializer
)

# --- ViewSets para Modelos Simples (CRUD) ---

class TipoProductoViewSet(viewsets.ModelViewSet):
    """Permite listar y gestionar los Tipos de Producto."""
    queryset = Tipo_Producto.objects.all().order_by('tipo_producto_nombre')
    serializer_class = TipoProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['tipo_producto_nombre']

class CategoriaInsumoViewSet(viewsets.ModelViewSet):
    """Permite listar y gestionar las Categorías de Insumo."""
    queryset = Categoria_Insumo.objects.all().order_by('categoria_insumo_nombre')
    serializer_class = CategoriaInsumoSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['categoria_insumo_nombre']

# --- ViewSets para Insumo y Producto ---

class InsumoViewSet(viewsets.ModelViewSet):
    """Permite listar y gestionar Insumos."""
    # Usamos select_related para optimizar la consulta y evitar N+1 queries
    queryset = Insumo.objects.all().select_related('categoria_insumo').order_by('insumo_nombre')
    serializer_class = InsumoSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['insumo_nombre', 'categoria_insumo__categoria_insumo_nombre']
    filterset_fields = ['categoria_insumo']

class ProductoViewSet(viewsets.ModelViewSet):
    """Permite listar y gestionar Productos, incluyendo sus 'recetas' (Insumos)."""
    # Usamos prefetch_related para obtener la relación inversa (Producto_X_Insumo)
    queryset = Producto.objects.all().select_related('tipo_producto').prefetch_related('producto_x_insumo_set').order_by('producto_nombre')
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['producto_nombre', 'producto_descripcion', 'tipo_producto__tipo_producto_nombre']
    filterset_fields = ['tipo_producto', 'producto_disponible']

class ProductoXInsumoViewSet(viewsets.ModelViewSet):
    """Permite gestionar las 'recetas' individuales (relaciones Producto-Insumo)."""
    queryset = Producto_X_Insumo.objects.all().select_related('producto', 'insumo')
    serializer_class = ProductoXInsumoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['producto', 'insumo']
