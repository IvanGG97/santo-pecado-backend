# cliente/urls.py
from django.urls import path
from .views import ClienteListCreateView, ClienteDetailView

urlpatterns = [
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
]