from rest_framework.routers import DefaultRouter
from .views import PromocionViewSet

# Creamos un router para registrar automáticamente las rutas del ViewSet.
router = DefaultRouter()

# Registramos el ViewSet de Promocion.
# Esto creará las rutas para:
# - /promociones/ (GET, POST)
# - /promociones/{pk}/ (GET, PUT, PATCH, DELETE)
router.register(r'promociones', PromocionViewSet, basename='promocion')

# Las URLs generadas por el router se incluyen en urlpatterns.
urlpatterns = router.urls