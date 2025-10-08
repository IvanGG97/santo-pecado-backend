from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        return Response({'error': 'Credenciales inválidas'}, status=400)



# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from .serializers import UserRegistroSerializer, UserSerializer, EmpleadoSerializer
# from .models import Empleado

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def registro_usuario(request):
#     print("✅ Llegó solicitud a /api/registro/")  # Debug
#     print("Datos recibidos:", request.data)  # Debug
    
#     serializer = UserRegistroSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
        
#         # Obtener datos del empleado relacionado
#         empleado_data = None
#         try:
#             empleado_data = EmpleadoSerializer(user.empleado).data
#         except Empleado.DoesNotExist:
#             print("⚠️ No se encontró empleado para el usuario")  # Debug
        
#         return Response({
#             'user': UserSerializer(user).data,
#             'empleado': empleado_data,
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_201_CREATED)
    
#     print("❌ Errores en serializer:", serializer.errors)  # Debug
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_usuario(request):
#     print("✅ Llegó solicitud a /api/login/")  # Debug
#     print("Datos recibidos:", request.data)  # Debug
    
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     user = authenticate(username=username, password=password)
    
#     if user is not None:
#         refresh = RefreshToken.for_user(user)
        
#         # Obtener datos del empleado si existe
#         empleado_data = None
#         roles = []
        
#         try:
#             empleado = user.empleado
#             empleado_data = EmpleadoSerializer(empleado).data
#             # Obtener roles del empleado
#             roles = [er.rol.rol_nombre for er in empleado.empleado_x_rol_set.all()]
#         except Empleado.DoesNotExist:
#             print("⚠️ No se encontró empleado para el usuario")  # Debug
#             pass
        
#         return Response({
#             'user': UserSerializer(user).data,
#             'empleado': empleado_data,
#             'roles': roles,
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_200_OK)
    
#     print("❌ Credenciales inválidas")  # Debug
#     return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def perfil_usuario(request):
#     user_data = UserSerializer(request.user).data
#     empleado_data = None
#     roles = []
    
#     try:
#         empleado = request.user.empleado
#         empleado_data = EmpleadoSerializer(empleado).data
#         roles = [er.rol.rol_nombre for er in empleado.empleado_x_rol_set.all()]
#     except Empleado.DoesNotExist:
#         pass
    
#     return Response({
#         'user': user_data,
#         'empleado': empleado_data,
#         'roles': roles
#     })