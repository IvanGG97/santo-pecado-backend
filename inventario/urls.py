from django.urls import path
from .views import (
    ProductoListCreateView, 
    ProductoDetailView, 
    TipoProductoListCreateView,
    TipoProductoDetailView # Importamos la vista de detalle
)

urlpatterns = [
    # --- Rutas de Productos ---
    path('productos/', ProductoListCreateView.as_view(), name='producto-list-create'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    
    # --- RUTAS PARA TIPO DE PRODUCTO (CORREGIDAS) ---
    # Para listar y crear
    path('tipos-producto/', TipoProductoListCreateView.as_view(), name='tipo-producto-list-create'),
    # Para ver, actualizar y eliminar un tipo específico
    path('tipos-producto/<int:pk>/', TipoProductoDetailView.as_view(), name='tipo-producto-detail'),
]

