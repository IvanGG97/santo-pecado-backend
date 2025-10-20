from django.urls import path
from .views import (
    RegisterView,
    ActivateAccountView,
    EmpleadoListView,
    EmpleadoDeleteView,
    EmpleadoUpdateView,
    RolListView,
    PasswordResetRequestView,    # ¡Importamos la nueva vista!
    PasswordResetConfirmView,   # ¡Importamos la nueva vista!
)

urlpatterns = [
    # Ruta para registrar un nuevo empleado
    path('register/', RegisterView.as_view(), name='register'),
    
    # Ruta para activar la cuenta usando el enlace del correo
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate-account'),
    
    # --- ¡NUEVAS RUTAS PARA RECUPERAR CONTRASEÑA! ---
    # Para solicitar el envío del correo de reseteo
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    # Para confirmar la nueva contraseña
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Rutas existentes para la gestión de empleados
    path('list/', EmpleadoListView.as_view(), name='empleado-list'),
    path('delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado-delete'),
    path('update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado-update'),
    path('roles/', RolListView.as_view(), name='rol-list'),
]

