from rest_framework import viewsets, permissions
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    # Ya maneja GET, POST, PUT, DELETE, y 404s automáticamente.
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
