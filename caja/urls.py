from django.urls import path, include
from .views import CajaList,CajaDetail

urlpatterns = [
    path('', CajaList.as_view(), name='caja-list'),
    path('<int:pk>/', CajaDetail.as_view(), name='caja-detail'),
]

