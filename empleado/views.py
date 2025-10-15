from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions
from .models import Empleado
from .serializers import (
    RegisterSerializer,
    EmpleadoSerializer,
    EmpleadoUpdateSerializer,
    RolSerializer
)

# --- VISTA DE REGISTRO ---
# Permite que cualquiera cree un nuevo User. La señal se encarga de crear el Empleado.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


# --- VISTA PARA LISTAR EMPLEADOS ---
# Devuelve la lista combinada de User y Empleado para la tabla del frontend.
class EmpleadoListView(generics.ListAPIView):
    queryset = User.objects.select_related('empleado').all().order_by('first_name')
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- VISTA PARA ACTUALIZAR UN EMPLEADO ---
# Usa el ID del perfil Empleado para encontrar y actualizar los datos.
class EmpleadoUpdateView(generics.UpdateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# --- VISTA PARA ELIMINAR UN EMPLEADO ---
# Usa el ID del User para encontrar y eliminar al usuario y su perfil en cascada.
class EmpleadoDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = EmpleadoSerializer # Solo se usa para la estructura, no para mostrar datos.
    permission_classes = [permissions.IsAdminUser]


# --- VISTA PARA LISTAR ROLES ---
# Devuelve la lista de Grupos para el menú desplegable del modal de edición.
class RolListView(generics.ListAPIView):
    queryset = Group.objects.all().order_by('name')
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAuthenticated]

