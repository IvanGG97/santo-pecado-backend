from django.urls import path
from .views import (
    VentaListCreateView,
    VentaDetailView,
    EstadoVentaListView
)

# Estas URLs definen los endpoints para la API de la app 'venta'.
# Todas las rutas estarán prefijadas con '/api/venta/' (o como lo hayas configurado).
urlpatterns = [
    # --- Rutas para Ventas ---
    
    # Endpoint para listar todas las ventas (GET) y para crear una nueva venta (POST).
    # GET -> /api/venta/ventas/
    # POST -> /api/venta/ventas/
    path('ventas/', VentaListCreateView.as_view(), name='venta-list-create'),
    
    # Endpoint para obtener (GET), actualizar (PUT/PATCH) o eliminar (DELETE) una venta específica.
    # El '<int:pk>' captura el ID de la venta desde la URL.
    # GET -> /api/venta/ventas/1/
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta-detail'),
    
    # --- Rutas para Modelos Relacionados ---
    
    # Endpoint para obtener la lista de todos los estados de venta disponibles.
    # Útil para los formularios en el frontend.
    # GET -> /api/venta/estados-venta/
    path('estados-venta/', EstadoVentaListView.as_view(), name='estado-venta-list'),
]
