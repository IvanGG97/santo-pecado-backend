from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TipoProductoViewSet,
    CategoriaInsumoViewSet,
    ProductoViewSet,
    InsumoViewSet,
    ProductoXInsumoViewSet
)

# Creamos un router para registrar automáticamente todas las rutas CRUD
router = DefaultRouter()

# Gestión de Productos y su configuración
router.register(r'productos', ProductoViewSet, basename='producto') 
router.register(r'tipos-producto', TipoProductoViewSet, basename='tipo-producto')

# Gestión de Insumos y su configuración
router.register(r'insumos', InsumoViewSet, basename='insumo')
router.register(r'categorias-insumo', CategoriaInsumoViewSet, basename='categoria-insumo')

# Gestión de las "Recetas" (relación Producto-Insumo)
router.register(r'recetas', ProductoXInsumoViewSet, basename='receta')

# Exportamos las rutas generadas por el router
urlpatterns = router.urls