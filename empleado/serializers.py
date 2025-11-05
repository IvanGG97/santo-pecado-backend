from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta
from .models import Empleado


# --- SERIALIZER DEL TOKEN CON LÓGICA DE BLOQUEO ---
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["is_staff"] = user.is_staff
        user_group = user.groups.first()
        token["rol"] = user_group.name if user_group else None
        return token

    def validate(self, attrs):
        username = attrs.get(self.username_field)
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed(
                "Credenciales inválidas o la cuenta no ha sido activada.",
                "no_active_account",
            )

        if (
            hasattr(user, "empleado")
            and user.empleado.lockout_until
            and user.empleado.lockout_until > timezone.now()
        ):
            raise AuthenticationFailed(
                "La cuenta ha sido bloqueada temporalmente por demasiados intentos fallidos.",
                "account_locked",
            )

        try:
            data = super().validate(attrs)
            if hasattr(user, "empleado"):
                user.empleado.failed_login_attempts = 0
                user.empleado.lockout_until = None
                user.empleado.save()
            return data
        except AuthenticationFailed:
            if hasattr(user, "empleado"):
                user.empleado.failed_login_attempts += 1
                user.empleado.save()

                if user.empleado.failed_login_attempts >= 3:
                    user.empleado.lockout_until = timezone.now() + timedelta(minutes=5)
                    user.empleado.save()
                    raise AuthenticationFailed(
                        "La cuenta ha sido bloqueada temporalmente.", "account_locked"
                    )
                else:
                    remaining_attempts = 3 - user.empleado.failed_login_attempts
                    error_message = f"Credenciales inválidas. Te quedan {remaining_attempts} intento(s)."
                    raise AuthenticationFailed(error_message, "no_active_account")

            raise AuthenticationFailed(
                "Credenciales inválidas o la cuenta no ha sido activada.",
                "no_active_account",
            )


# --- EL RESTO DE TUS SERIALIZERS (SIN CAMBIOS) ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    dni = serializers.CharField(write_only=True, required=False, allow_blank=True)
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "dni",
            "telefono",
        )

    def create(self, validated_data):
        dni_data = validated_data.pop("dni", None)
        telefono_data = validated_data.pop("telefono", None)
        user = User.objects.create_user(**validated_data)
        try:
            # 1. Asignar el rol "Cliente" por defecto (creado por la migración)
            cliente_group = Group.objects.get(name="Cliente")
            user.groups.add(cliente_group)

            # 2. Asignar también al campo 'rol' del modelo Empleado
            if hasattr(user, "empleado"):
                user.empleado.dni = dni_data
                user.empleado.telefono = telefono_data
                user.empleado.rol = cliente_group  # <-- Asignar el rol aquí
                user.empleado.save()

        except Group.DoesNotExist:

            print(
                "ERROR: El grupo 'Cliente' no existe. Por favor corre las migraciones."
            )
            pass

        return user


class EmpleadoSerializer(serializers.ModelSerializer):
    empleado_id = serializers.IntegerField(source="empleado.id", read_only=True)
    rol = serializers.StringRelatedField(source="empleado.rol")
    dni = serializers.CharField(source="empleado.dni", read_only=True)
    telefono = serializers.CharField(source="empleado.telefono", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "empleado_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
            "dni",
            "telefono",
        ]


class EmpleadoUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    rol = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Empleado
        fields = ["dni", "telefono", "rol", "first_name", "last_name"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        instance.dni = validated_data.get("dni", instance.dni)
        instance.telefono = validated_data.get("telefono", instance.telefono)
        new_rol = validated_data.get("rol", instance.rol)
        instance.rol = new_rol
        instance.save()
        if new_rol:
            user.groups.set([new_rol])
            if new_rol.name == "Admin":
                user.is_staff = True
            else:
                user.is_staff = False
        else:
            user.groups.clear()
            user.is_staff = False
        user.save()
        return instance


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
