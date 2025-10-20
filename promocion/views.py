from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Promocion
from .serializers import PromocionReadSerializer, PromocionWriteSerializer

class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.prefetch_related('productos_promocion__producto').all().order_by('-id')

    def get_serializer_class(self):
        # Si la acción es para leer (list o retrieve), usamos el serializer de lectura.
        if self.action in ['list', 'retrieve']:
            return PromocionReadSerializer
        # Para cualquier otra acción (create, update, patch), usamos el de escritura.
        return PromocionWriteSerializer

    # --- CÓDIGO DE DIAGNÓSTICO AÑADIDO ---
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n----------- DETALLES DEL ERROR DE VALIDACIÓN (CREAR PROMOCIÓN) -----------")
            print("Datos recibidos por el backend:")
            print(request.data)
            print("\nErrores encontrados por el serializer:")
            print(serializer.errors)
            print("----------------------------------------------------------------------\n")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            print("\n----------- DETALLES DEL ERROR DE VALIDACIÓN (EDITAR PROMOCIÓN) -----------")
            print("Datos recibidos por el backend:")
            print(request.data)
            print("\nErrores encontrados por el serializer:")
            print(serializer.errors)
            print("-----------------------------------------------------------------------\n")
        return super().update(request, *args, **kwargs)

