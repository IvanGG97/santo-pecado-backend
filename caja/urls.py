from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CajaViewSet

# Crea un router y registra el ViewSet.
# Esto genera automáticamente las rutas estándar (listar, detalle, etc.)
router = DefaultRouter()
router.register(r'cajas', CajaViewSet, basename='caja')

# El router.urls incluye todas las rutas estándar y las personalizadas (@action)
urlpatterns = router.urls