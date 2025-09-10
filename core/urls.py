
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cajas/',include('caja.urls')),
    path('api/clientes/',include('cliente.urls')),
]
