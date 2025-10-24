from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Producto, Tipo_Producto, Insumo, Categoria_Insumo
from .serializers import (
    ProductoSerializer, ProductoWriteSerializer, TipoProductoSerializer,
    InsumoReadSerializer, InsumoWriteSerializer, CategoriaInsumoSerializer
)

# --- VISTA PARA LISTAR Y CREAR PRODUCTOS ---
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all().order_by('producto_nombre')
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'POST': return ProductoWriteSerializer
        return ProductoSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST': return [permissions.IsAdminUser()]
        return super().get_permissions()

# --- VISTA PARA EDITAR/VER/BORRAR PRODUCTOS ---
class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductoWriteSerializer
        return ProductoSerializer

# --- Vistas de Tipo de Producto ---
class TipoProductoListCreateView(generics.ListCreateAPIView):
    queryset = Tipo_Producto.objects.all().order_by('tipo_producto_nombre')
    serializer_class = TipoProductoSerializer
    permission_classes = [permissions.IsAdminUser]

class TipoProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tipo_Producto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = [permissions.IsAdminUser]


# --- Vistas para Insumos ---
class InsumoListCreateView(generics.ListCreateAPIView):
    queryset = Insumo.objects.all().order_by('insumo_nombre')
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InsumoWriteSerializer
        return InsumoReadSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class InsumoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insumo.objects.all()
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return InsumoWriteSerializer
        return InsumoReadSerializer

# --- Vistas para Categorías de Insumos ---
class CategoriaInsumoListCreateView(generics.ListCreateAPIView):
    queryset = Categoria_Insumo.objects.all().order_by('categoria_insumo_nombre')
    serializer_class = CategoriaInsumoSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoriaInsumoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria_Insumo.objects.all()
    serializer_class = CategoriaInsumoSerializer
    permission_classes = [permissions.IsAdminUser]

