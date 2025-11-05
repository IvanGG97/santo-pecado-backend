from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Empleado
from .serializers import (
    RegisterSerializer,
    EmpleadoSerializer,
    EmpleadoUpdateSerializer,
    RolSerializer
)
from .serializers import RegisterSerializer, PasswordResetConfirmSerializer

# --- VISTA PARA LISTAR EMPLEADOS ---
# Devuelve la lista combinada de User y Empleado para la tabla del frontend.
class EmpleadoListView(generics.ListAPIView):
    queryset = User.objects.select_related('empleado').all().order_by('first_name')
    serializer_class = EmpleadoSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- VISTA PARA ACTUALIZAR UN EMPLEADO ---
# Usa el ID del perfil Empleado para encontrar y actualizar los datos.
class EmpleadoUpdateView(generics.UpdateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# --- VISTA PARA ELIMINAR UN EMPLEADO ---
# Usa el ID del User para encontrar y eliminar al usuario y su perfil en cascada.
class EmpleadoDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = EmpleadoSerializer # Solo se usa para la estructura, no para mostrar datos.
    permission_classes = [permissions.IsAdminUser]


# --- VISTA PARA LISTAR ROLES ---
# Devuelve la lista de Grupos para el menú desplegable del modal de edición.
class RolListView(generics.ListAPIView):
    queryset = Group.objects.all().order_by('name')
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        # Creamos el usuario pero lo marcamos como inactivo
        user = serializer.save()
        user.is_active = False
        user.save()

        # Generamos el token y el ID de usuario codificado
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construimos el enlace de activación que apuntará a nuestro frontend
        activation_link = f"http://localhost:3000/activar-cuenta/{uid}/{token}/"
        
        # Preparamos y enviamos el correo (se imprimirá en la consola)
        subject = 'Activa tu cuenta en Santo Pecado'
        message = f'Hola {user.first_name},\n\nPor favor, haz clic en el siguiente enlace para activar tu cuenta:\n{activation_link}\n\nGracias,\nEl equipo de Santo Pecado.'
        
        send_mail(
            subject,
            message,
            'no-reply@santopecado.com', # Remitente
            [user.email], # Destinatario
            fail_silently=False,
        )

# --- ¡NUEVA VISTA DE ACTIVACIÓN! ---
class ActivateAccountView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': '¡Cuenta activada exitosamente! Ya puedes iniciar sesión.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'El enlace de activación es inválido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)


# --- VISTA PARA SOLICITAR EL RESETEO DE CONTRASEÑA ---
class PasswordResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            user = None

        # Por seguridad, siempre devolvemos un mensaje de éxito,
        # incluso si el correo no existe, para no revelar información.
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # El enlace apuntará a la nueva página que crearemos en el frontend
            reset_link = f"http://localhost:3000/restablecer-contrasena/{uid}/{token}/"
            
            subject = 'Restablece tu contraseña en Santo Pecado'
            message = f'Hola {user.first_name},\n\nHaz clic en el siguiente enlace para restablecer tu contraseña:\n{reset_link}\n\nSi no solicitaste esto, ignora este correo.'
            
            send_mail(subject, message, 'no-reply@santopecado.com', [user.email])

        return Response({'detail': 'Si existe una cuenta asociada a este correo, recibirás un enlace para recuperar tu contraseña.'}, status=status.HTTP_200_OK)


# --- VISTA PARA CONFIRMAR LA NUEVA CONTRASEÑA ---
class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, serializer.validated_data['token']):
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'detail': '¡Contraseña restablecida con éxito!'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'El enlace es inválido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)