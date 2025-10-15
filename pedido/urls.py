from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, EstadoPedidoViewSet

router = DefaultRouter()

router.register(r'pedidos', PedidoViewSet, basename='pedido')

router.register(r'estados', EstadoPedidoViewSet, basename='estado-pedido')

urlpatterns = [
    path('', include(router.urls)),
]
