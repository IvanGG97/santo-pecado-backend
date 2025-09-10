from django.urls import path, include
from .views import ClientesList,ClienteDetail
urlpatterns = [
    path('', ClientesList.as_view(), name='clientes-list'),
    path('<int:pk>/', ClienteDetail.as_view(), name='cliente-detail'),
]
