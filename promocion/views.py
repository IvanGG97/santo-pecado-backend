from rest_framework import viewsets
from .models import Promocion
from .serialziers import PromocionSerializer

class PromocionViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver, crear, editar y eliminar promociones.
    - Al crear o actualizar, se debe enviar una lista de IDs de productos en el campo `productos_ids`.
    - Al obtener una promoción, se mostrarán los detalles completos de los productos asociados.
    """
    serializer_class = PromocionSerializer
    
    # El queryset base para este ViewSet.
    # Usamos prefetch_related para optimizar la consulta y evitar el problema N+1
    # al obtener los productos relacionados con cada promoción.
    # 'productos_promocion' es el related_name en el modelo Producto_Promocion.
    # '__producto' sigue la relación para precargar también el objeto Producto.
    queryset = Promocion.objects.prefetch_related('productos_promocion__producto').all()
