from django.urls import path
from .views import (
    RegisterView,
    EmpleadoListView,
    EmpleadoDeleteView,
    EmpleadoUpdateView,
    RolListView  # Importamos la nueva vista para listar roles
)

# Este urlpatterns define las rutas específicas para la app 'empleado'
# Todas estas rutas estarán prefijadas con '/api/empleado/' 
# según la configuración en el urls.py principal de tu proyecto.
urlpatterns = [
    # Ruta para registrar un nuevo empleado
    # El frontend hará una petición POST a: /api/empleado/register/
    path('register/', RegisterView.as_view(), name='register'),
    
    # Ruta para obtener la lista completa de empleados
    # El frontend hará una petición GET a: /api/empleado/list/
    path('list/', EmpleadoListView.as_view(), name='empleado-list'),
    
    # Ruta para eliminar un empleado específico por su ID (pk = Primary Key)
    # El frontend hará una petición DELETE a, por ejemplo: /api/empleado/delete/5/
    path('delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado-delete'),
    
    # Ruta para actualizar a un empleado
    # El frontend hará una petición PUT o PATCH a, por ejemplo: /api/empleado/update/5/
    # Nota: El 'pk' aquí se refiere al ID del perfil Empleado, no del User.
    path('update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado-update'),

    # Ruta para obtener la lista de roles (Grupos) disponibles
    # El frontend hará una petición GET a: /api/empleado/roles/
    path('roles/', RolListView.as_view(), name='rol-list'),
]

