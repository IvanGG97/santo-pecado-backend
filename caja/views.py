from rest_framework import generics, permissions, status, views, serializers
from rest_framework.response import Response
from decimal import Decimal # <-- 1. IMPORTAR DECIMAL
from .models import Caja
from .serializers import CajaListSerializer, CajaCreateSerializer, CajaCloseSerializer

class CajaHistoryView(generics.ListAPIView):
    queryset = Caja.objects.all().select_related('empleado__user').order_by('-caja_fecha_hora_apertura')
    serializer_class = CajaListSerializer
    permission_classes = [permissions.IsAuthenticated]

class CajaStatusView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            caja_abierta = Caja.objects.get(caja_estado=True)
            serializer = CajaListSerializer(caja_abierta, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Caja.DoesNotExist:
            try:
                ultima_caja_cerrada = Caja.objects.filter(caja_estado=False).latest('caja_fecha_hora_cierre')
                monto_sugerido = ultima_caja_cerrada.caja_saldo_final
            except Caja.DoesNotExist:
                # --- 2. CORREGIR EL TIPO DE DATO ---
                monto_sugerido = Decimal('0.00') # <-- CORREGIDO (era 0.00)
            
            return Response({
                "caja_estado": False, 
                "detail": "No hay ninguna caja abierta.",
                "monto_sugerido_apertura": monto_sugerido
            }, status=status.HTTP_200_OK)

        except Caja.MultipleObjectsReturned:
            return Response({"caja_estado": False, "detail": "Error: Hay múltiples cajas abiertas. Cierre todas manualmente."}, status=status.HTTP_400_BAD_REQUEST)

class AbrirCajaView(generics.CreateAPIView):
    queryset = Caja.objects.none()
    serializer_class = CajaCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if Caja.objects.filter(caja_estado=True).exists():
            raise serializers.ValidationError("Ya hay una caja abierta. Debe cerrarla antes de abrir una nueva.")
        
        if not hasattr(self.request.user, 'empleado'):
            raise serializers.ValidationError("Usuario no asociado a un empleado.")
        empleado = self.request.user.empleado

        monto_inicial_enviado = serializer.validated_data.get('caja_monto_inicial')
        monto_final_a_usar = Decimal('0.00') # <-- CORREGIDO (era 0.00)

        try:
            ultima_caja_cerrada = Caja.objects.filter(caja_estado=False).latest('caja_fecha_hora_cierre')
            monto_final_a_usar = ultima_caja_cerrada.caja_saldo_final
        except Caja.DoesNotExist:
            if monto_inicial_enviado is None or monto_inicial_enviado < 0:
                 raise serializers.ValidationError("Es la primera caja. Debe proveer un monto inicial válido.")
            monto_final_a_usar = monto_inicial_enviado
        
        serializer.save(empleado=empleado, caja_monto_inicial=monto_final_a_usar)

class CerrarCajaView(generics.UpdateAPIView):
    queryset = Caja.objects.filter(caja_estado=True)
    serializer_class = CajaCloseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return self.get_queryset().get()
        except Caja.DoesNotExist:
            raise serializers.ValidationError("No hay ninguna caja abierta para cerrar.")
        except Caja.MultipleObjectsReturned:
            raise serializers.ValidationError("Error: Hay múltiples cajas abiertas. Cierrelas manualmente.")