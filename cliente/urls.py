from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

# Creamos un router para registrar automáticamente las rutas del ViewSet.
router = DefaultRouter()

# Registramos el ViewSet de Cliente.
# Esto creará las rutas para:
# - /clientes/ (GET para listar, POST para crear)
# - /clientes/{pk}/ (GET para detalle, PUT/PATCH para actualizar, DELETE para borrar)
router.register(r'clientes', ClienteViewSet, basename='cliente')

# Las URLs generadas por el router se incluyen en urlpatterns.
urlpatterns = router.urls
