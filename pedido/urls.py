from django.urls import path
from .views import PedidoListCreateView, PedidoDetailView, EstadoPedidoListView

urlpatterns = [
    # Ruta para listar y crear pedidos
    # GET, POST -> /api/pedido/pedidos/
    path('pedidos/', PedidoListCreateView.as_view(), name='pedido-list-create'),
    
    # Ruta para ver, actualizar y eliminar un pedido específico
    # GET, PUT, PATCH, DELETE -> /api/pedido/pedidos/5/
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),

    # Ruta para obtener la lista de estados de pedido
    # GET -> /api/pedido/estados/
    path('estados/', EstadoPedidoListView.as_view(), name='estado-pedido-list'),
]
