from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Caja
from .serializers import CajaSerializer # Necesitamos el serializer previamente definido

class CajaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar y consultar Cajas. 
    Implementa acciones específicas para Abrir y Cerrar la caja.
    """
    queryset = Caja.objects.all().order_by('-caja_fecha_hora_apertura')
    serializer_class = CajaSerializer
    permission_classes = [permissions.IsAuthenticated]

    # --- Permite solo la consulta de una caja por ID (GET) ---
    # La creación se manejará con la acción 'abrir'
    # La actualización y eliminación se deshabilitan por seguridad, 
    # ya que modificar historiales de caja es peligroso.
    http_method_names = ['get', 'head', 'options']

    # ----------------------------------------------------------------------
    # ACCIÓN PERSONALIZADA: /caja/abrir/
    # Se usa para iniciar una nueva caja.
    # ----------------------------------------------------------------------
    @action(detail=False, methods=['post'])
    def abrir(self, request):
        """
        Abre una nueva caja. Requiere 'empleado_x_rol' y 'caja_monto_inicial'.
        La validación de caja abierta la maneja el Serializer.
        """
        # El serializer solo recibe los campos necesarios para la apertura
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # La creación se realiza normalmente a través del serializer
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------------------------------------------------------------------
    # ACCIÓN PERSONALIZADA: /caja/{pk}/cerrar/
    # Se usa para cerrar una caja existente.
    # ----------------------------------------------------------------------
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """
        Cierra una caja específica. Requiere el ID de la caja (pk) y opcionalmente
        'caja_saldo_final' y 'caja_observacion' en el cuerpo de la petición.
        """
        caja = get_object_or_404(Caja, pk=pk)

        if not caja.caja_estado:
            return Response({'error': 'La caja ya se encuentra cerrada.'}, status=status.HTTP_400_BAD_REQUEST)

        # Datos a actualizar para el cierre
        datos_cierre = {
            'caja_estado': False, # Cambiar estado a cerrado
            'caja_fecha_hora_cierre': timezone.now(),
            'caja_saldo_final': request.data.get('caja_saldo_final'), # Saldo final reportado
            'caja_observacion': request.data.get('caja_observacion', caja.caja_observacion)
        }
        
        # Opcional: Aquí podrías añadir lógica para calcular el 'caja_saldo_final' 
        # automáticamente sumando todos los Ingresos y restando Egresos/Ventas.
        # Por ahora, se espera que el frontend o una lógica interna lo provea.

        # Actualizar la instancia de la caja con los datos de cierre
        serializer = self.get_serializer(caja, data=datos_cierre, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------------------------------------------------------------------
    # ACCIÓN PERSONALIZADA: /caja/abierta/
    # Se usa para obtener la caja que está actualmente activa para el usuario (si aplica).
    # ----------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def abierta(self, request):
        """
        Obtiene la última caja que se encuentra en estado 'abierta'.
        """
        # Nota: Aquí se necesitaría lógica de negocio avanzada si tuvieras el Empleado
        # autenticado. Por simplicidad, busca la última caja abierta.
        try:
            caja_abierta = Caja.objects.filter(caja_estado=True).latest('caja_fecha_hora_apertura')
            serializer = self.get_serializer(caja_abierta)
            return Response(serializer.data)
        except Caja.DoesNotExist:
            return Response({'error': 'No hay ninguna caja abierta en este momento.'}, status=status.HTTP_404_NOT_FOUND)
