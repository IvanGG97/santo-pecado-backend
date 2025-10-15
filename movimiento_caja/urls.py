from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EgresoViewSet, IngresoViewSet

# Crea un router y registra nuestros ViewSets.
# El DefaultRouter maneja automáticamente la generación de rutas CRUD.
router = DefaultRouter()
router.register(r'egresos', EgresoViewSet, basename='egreso')
router.register(r'ingresos', IngresoViewSet, basename='ingreso')

urlpatterns = [
    # Incluye las URLs generadas por el router para egresos e ingresos
    path('', include(router.urls)),
]
