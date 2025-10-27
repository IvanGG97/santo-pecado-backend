from rest_framework import viewsets
from .models import Promocion
# Importamos los serializers
from .serializers import PromocionReadSerializer, PromocionWriteSerializer

class PromocionViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver, crear, editar y eliminar promociones.
    Ahora solo acepta datos en formato JSON.
    """
    queryset = Promocion.objects.prefetch_related('productos_promocion__producto').all().order_by('-id')
    # Ya no necesitamos parser_classes para FormData

    def get_serializer_class(self):
        # Si la acción es para leer (list o retrieve), usamos el serializer de lectura.
        if self.action in ['list', 'retrieve']:
            return PromocionReadSerializer
        # Para cualquier otra acción (create, update, patch), usamos el de escritura.
        return PromocionWriteSerializer
    
    # Los métodos create y update de diagnóstico han sido eliminados
    # y se revierte al comportamiento estándar de ModelViewSet.

