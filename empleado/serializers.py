from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Empleado

# ... MyTokenObtainPairSerializer (sin cambios) ...
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['is_staff'] = user.is_staff
        user_group = user.groups.first()
        token['rol'] = user_group.name if user_group else None
        return token

# --- RegisterSerializer (MODIFICADO) ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    # 1. Añadimos los nuevos campos que vendrán desde el frontend.
    dni = serializers.CharField(write_only=True, required=False, allow_blank=True)
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        # 2. Incluimos los nuevos campos en la lista.
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'dni', 'telefono')

    def create(self, validated_data):
        # 3. Separamos los datos del Empleado de los datos del User.
        dni_data = validated_data.pop('dni', None)
        telefono_data = validated_data.pop('telefono', None)
        
        # 4. Creamos el objeto User con los datos restantes.
        user = User.objects.create_user(**validated_data)

        # 5. La señal 'post_save' en models.py ya creó un perfil Empleado vacío.
        #    Ahora lo actualizamos con los datos adicionales.
        if hasattr(user, 'empleado'):
            user.empleado.dni = dni_data
            user.empleado.telefono = telefono_data
            user.empleado.save()
            
        return user

# ... EmpleadoSerializer, EmpleadoUpdateSerializer, RolSerializer (sin cambios) ...
class EmpleadoSerializer(serializers.ModelSerializer):
    empleado_id = serializers.IntegerField(source='empleado.id', read_only=True)
    rol = serializers.StringRelatedField(source='empleado.rol')
    dni = serializers.CharField(source='empleado.dni', read_only=True)
    telefono = serializers.CharField(source='empleado.telefono', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'empleado_id', 'username', 'email', 'first_name', 'last_name', 'rol', 'dni', 'telefono']

class EmpleadoUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    rol = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Empleado
        fields = ['dni', 'telefono', 'rol', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        # Actualiza los datos del User (nombre, apellido)
        user_data = validated_data.pop('user', {})
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        
        # Actualiza los campos del perfil Empleado
        instance.dni = validated_data.get('dni', instance.dni)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        
        # --- LÓGICA DE SINCRONIZACIÓN DE ROL Y PERMISOS ---
        new_rol = validated_data.get('rol', instance.rol)
        
        # 1. Actualiza el rol en el perfil del Empleado
        instance.rol = new_rol
        instance.save()
        
        # 2. Sincroniza los grupos del User y el estado de 'staff'
        if new_rol:
            user.groups.set([new_rol])
            # Si el rol es 'Admin', se convierte en staff. Si no, no lo es.
            if new_rol.name == 'Admin':
                user.is_staff = True
            else:
                user.is_staff = False
        else:
            # Si se asigna "Sin Rol", se eliminan los grupos y el status de staff.
            user.groups.clear()
            user.is_staff = False
            
        # Guardamos el usuario para persistir los cambios en is_staff y los grupos.
        user.save()
            
        return instance

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
