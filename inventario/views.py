from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Producto, Tipo_Producto, Insumo, Categoria_Insumo,Producto_X_Insumo
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

    # --- MÉTODO DESTROY SOBREESCRITO (PARA PRODUCTOS) ---
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # Obtiene el producto a borrar

        # Busca si este producto está referenciado en algún Detalle_Pedido
        pedidos_relacionados = Detalle_Pedido.objects.filter(producto=instance)

        if pedidos_relacionados.exists():
            # Si está en uso, recopila los IDs de los pedidos (o fechas, si prefieres)
            ids_pedidos = list(set([detalle.pedido.id for detalle in pedidos_relacionados.select_related('pedido')]))
            ids_pedidos_str = ', '.join(map(str, ids_pedidos)) # Convertimos IDs a string para el mensaje

            # Devuelve un error 400 con la lista de IDs de pedidos
            mensaje = f"Este producto no se puede borrar porque está incluido en los siguientes pedidos: N° {ids_pedidos_str}."
            return Response(
                {"detail": mensaje, "pedidos": ids_pedidos}, # Enviamos 'detail' y la lista de IDs
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si no está en uso en ningún pedido, procede con la eliminación normal
        return super().destroy(request, *args, **kwargs)

# --- Vistas de Tipo de Producto ---
class TipoProductoListCreateView(generics.ListCreateAPIView):
    queryset = Tipo_Producto.objects.all().order_by('tipo_producto_nombre')
    serializer_class = TipoProductoSerializer
    # permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        """
        Permisos dinámicos:
        - GET: Todos los autenticados (para la Carta).
        - POST: Solo Admins.
        """
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

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

    # --- MÉTODO DESTROY SOBREESCRITO ---
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # Obtiene el insumo a borrar
        
        # Busca si este insumo está siendo usado en alguna receta
        productos_relacionados = Producto_X_Insumo.objects.filter(insumo=instance)
        
        if productos_relacionados.exists():
            # Si está en uso, recopila los nombres de los productos
            nombres_productos = [
                relacion.producto.producto_nombre 
                for relacion in productos_relacionados.select_related('producto') # Optimiza la consulta
            ]
            # Devuelve un error 400 con la lista de productos
            mensaje = f"Este insumo no se puede borrar porque está en uso en los siguientes productos: {', '.join(nombres_productos)}."
            return Response(
                {"detail": mensaje, "productos": nombres_productos}, # Enviamos 'detail' para DRF y 'productos' para el front
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Si no está en uso, procede con la eliminación normal
        return super().destroy(request, *args, **kwargs)

# --- Vistas para Categorías de Insumos ---
class CategoriaInsumoListCreateView(generics.ListCreateAPIView):
    queryset = Categoria_Insumo.objects.all().order_by('categoria_insumo_nombre')
    serializer_class = CategoriaInsumoSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoriaInsumoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria_Insumo.objects.all()
    serializer_class = CategoriaInsumoSerializer
    permission_classes = [permissions.IsAdminUser]

    # --- MÉTODO DESTROY SOBREESCRITO (PARA CATEGORÍAS) ---
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() 
        insumos_relacionados = instance.insumo_set.all() 

        if insumos_relacionados.exists():
            nombres_insumos = [insumo.insumo_nombre for insumo in insumos_relacionados]
            mensaje = f"No se puede borrar la categoría porque contiene a estos insumos: {', '.join(nombres_insumos)}."
            return Response(
                {"detail": mensaje, "insumos": nombres_insumos}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)

