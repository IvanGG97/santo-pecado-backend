from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Caja
from .serializers import CajaSerializer


# Create your views here.

class CajaList(APIView):
    def get(self, request, format=None):
        cajas = Caja.objects.all()
        serializer = CajaSerializer(cajas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CajaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CajaDetail(APIView):
    def get_object(self, pk):
        try:
            return Caja.objects.get(pk=pk)
        except Caja.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk, format=None):
        caja = self.get_object(pk)
        caja.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    def put(self, request, pk, format=None):
        caja = self.get_object(pk)
        serializer = CajaSerializer(caja, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
