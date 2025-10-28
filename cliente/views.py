from rest_framework import generics, permissions, filters # Importar filters
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar (con búsqueda) y crear Clientes.
    - GET /api/cliente/clientes/ : Lista todos los clientes.
    - GET /api/cliente/clientes/?search=juan : Busca clientes por nombre o teléfono.
    - POST /api/cliente/clientes/ : Crea un nuevo cliente.
    """
    queryset = Cliente.objects.all().order_by('cliente_nombre', 'cliente_apellido') # Ordenar alfabéticamente
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated] # O el permiso que necesites (ej: IsAdminUser)
    
    # --- Añadir Funcionalidad de Búsqueda ---
    filter_backends = [filters.SearchFilter]
    search_fields = ['cliente_nombre', 'cliente_telefono', 'cliente_apellido', 'cliente_dni','cliente_direccion'] # Campos por los que se puede buscar
    # --- Fin Búsqueda ---

# Opcional: Si necesitas vistas separadas para detalle (ver, editar, borrar uno específico)
# class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cliente.objects.all()
#     serializer_class = ClienteSerializer
#     permission_classes = [permissions.IsAuthenticated] # O IsAdminUser
class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver (GET), actualizar (PUT/PATCH) o eliminar (DELETE)
    un cliente específico por su ID.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
