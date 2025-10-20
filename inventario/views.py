from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Producto, Tipo_Producto
from .serializers import ProductoSerializer, ProductoWriteSerializer, TipoProductoSerializer

# --- VISTA PARA LISTAR Y CREAR PRODUCTOS (CON DIAGNÓSTICO) ---
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all().order_by('producto_nombre')
    permission_classes = [permissions.IsAuthenticated]
    # Forzamos a la vista a escuchar solo el formato de subida de archivos
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'POST': return ProductoWriteSerializer
        return ProductoSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST': return [permissions.IsAdminUser()]
        return super().get_permissions()

    # --- CÓDIGO DE DIAGNÓSTICO PROFUNDO ---
    def create(self, request, *args, **kwargs):
        print("\n----------- DIAGNÓSTICO PROFUNDO (CREAR PRODUCTO) -----------")
        print("HEADERS DE LA PETICIÓN:")
        print(request.headers)
        print("\nCONTENIDO DE request.POST (DATOS DE TEXTO RECIBIDOS):")
        print(request.POST)
        print("\nCONTENIDO DE request.FILES (ARCHIVOS RECIBIDOS):")
        print(request.FILES)
        print("-----------------------------------------------------------\n")

        # Intentamos validar los datos como siempre
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("--- ERRORES ENCONTRADOS POR EL SERIALIZER ---")
            print(serializer.errors)
            print("---------------------------------------------\n")
        
        return super().create(request, *args, **kwargs)

# ... El resto de tus vistas se quedan igual ...
class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductoWriteSerializer
        return ProductoSerializer

    # --- CÓDIGO DE DIAGNÓSTICO ---
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            print("\n----------- DETALLES DEL ERROR DE VALIDACIÓN (EDITAR) -----------")
            print("Datos recibidos por el backend:")
            print(request.data)
            print("\nErrores encontrados por el serializer:")
            print(serializer.errors)
            print("-----------------------------------------------------------------\n")
        return super().update(request, *args, **kwargs)


# --- Vistas de Tipo de Producto (sin cambios) ---
class TipoProductoListCreateView(generics.ListCreateAPIView):
    queryset = Tipo_Producto.objects.all().order_by('tipo_producto_nombre')
    serializer_class = TipoProductoSerializer
    permission_classes = [permissions.IsAdminUser]

class TipoProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tipo_Producto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = [permissions.IsAdminUser]






# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# from .models import Producto, Tipo_Producto
# from .serializers import ProductoSerializer, ProductoWriteSerializer, TipoProductoSerializer

# # --- VISTA PARA LISTAR Y CREAR PRODUCTOS (CON DIAGNÓSTICO) ---
# class ProductoListCreateView(generics.ListCreateAPIView):
#     queryset = Producto.objects.all().order_by('producto_nombre')
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]

#     def get_serializer_class(self):
#         if self.request.method == 'POST': return ProductoWriteSerializer
#         return ProductoSerializer
    
#     def get_permissions(self):
#         if self.request.method == 'POST': return [permissions.IsAdminUser()]
#         return super().get_permissions()

#     # --- CÓDIGO DE DIAGNÓSTICO ---
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             print("\n----------- DETALLES DEL ERROR DE VALIDACIÓN (CREAR) -----------")
#             print("Datos recibidos por el backend:")
#             print(request.data)
#             print("\nErrores encontrados por el serializer:")
#             print(serializer.errors)
#             print("----------------------------------------------------------------\n")
#         return super().create(request, *args, **kwargs)

# # --- VISTA PARA EDITAR/VER/BORRAR PRODUCTOS (CON DIAGNÓSTICO) ---
# class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Producto.objects.all()
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]

#     def get_serializer_class(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             return ProductoWriteSerializer
#         return ProductoSerializer

#     # --- CÓDIGO DE DIAGNÓSTICO ---
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if not serializer.is_valid():
#             print("\n----------- DETALLES DEL ERROR DE VALIDACIÓN (EDITAR) -----------")
#             print("Datos recibidos por el backend:")
#             print(request.data)
#             print("\nErrores encontrados por el serializer:")
#             print(serializer.errors)
#             print("-----------------------------------------------------------------\n")
#         return super().update(request, *args, **kwargs)


# # --- Vistas de Tipo de Producto (sin cambios) ---
# class TipoProductoListCreateView(generics.ListCreateAPIView):
#     queryset = Tipo_Producto.objects.all().order_by('tipo_producto_nombre')
#     serializer_class = TipoProductoSerializer
#     permission_classes = [permissions.IsAdminUser]

# class TipoProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tipo_Producto.objects.all()
#     serializer_class = TipoProductoSerializer
#     permission_classes = [permissions.IsAdminUser]
