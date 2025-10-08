from rest_framework import serializers
from django.contrib.auth.models import User
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user





# from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
# from .models import Empleado, Empleado_x_rol, Rol

# class UserRegistroSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     rol = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'rol')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
#         return attrs

#     def create(self, validated_data):
#         rol_nombre = validated_data.pop('rol', None)
#         validated_data.pop('password2')
        
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data.get('email', ''),
#             password=validated_data['password'],
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', '')
#         )
        
#         # Asignar rol al empleado si se especificó
#         if rol_nombre:
#             try:
#                 rol = Rol.objects.get(rol_nombre=rol_nombre)
#                 # Crear o obtener el empleado
#                 empleado, created = Empleado.objects.get_or_create(
#                     usuario=user,
#                     defaults={
#                         'empleado_dni': user.username,
#                         'empleado_nombre': user.first_name or user.username,
#                         'empleado_apellido': user.last_name or '',
#                         'empleado_telefono': ''
#                     }
#                 )
#                 Empleado_x_rol.objects.create(empleado=empleado, rol=rol)
#             except (Rol.DoesNotExist, Exception as e):
#                 print(f"Error al asignar rol: {e}")
        
#         return user

# class EmpleadoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Empleado
#         fields = ('id', 'empleado_dni', 'empleado_nombre', 'empleado_apellido', 'empleado_telefono')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name')