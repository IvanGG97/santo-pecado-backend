from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Empleado

# Para una mejor experiencia, vamos a integrar el perfil 'Empleado'
# directamente en la vista del 'User' en el panel de administrador.

# 1. Desregistramos el UserAdmin por defecto de Django.
admin.site.unregister(User)

# 2. Creamos una clase 'Inline' para el perfil de Empleado.
#    Esto nos permitirá ver y editar los campos de Empleado (DNI, teléfono, rol)
#    DENTRO del formulario del User.
class EmpleadoInline(admin.StackedInline):
    model = Empleado
    can_delete = False
    verbose_name_plural = 'Perfil de Empleado'
    fk_name = 'user'
    fields = ('dni', 'telefono', 'rol') # Campos a mostrar

# 3. Creamos una nueva clase UserAdmin que incluye nuestro perfil de Empleado.
class CustomUserAdmin(UserAdmin):
    inlines = (EmpleadoInline, )

    # Función para mostrar el rol en la lista de usuarios del admin.
    def get_rol(self, instance):
        # Usamos hasattr para evitar errores si el perfil de empleado aún no existe.
        if hasattr(instance, 'empleado') and instance.empleado.rol:
            return instance.empleado.rol.name
        return "Sin rol"
    get_rol.short_description = 'Rol'

    # Añadimos nuestro campo 'get_rol' a la lista de columnas a mostrar.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol')
    list_select_related = ('empleado__rol', )


# 4. Finalmente, registramos el modelo User con nuestra configuración personalizada.
admin.site.register(User, CustomUserAdmin)

# 5. Registramos el modelo Empleado por separado para que autocomplete_fields funcione.
#    Este registro no aparecerá como una entrada principal en el admin si no se desea,
#    pero es necesario para que otros ModelAdmin puedan buscar empleados.
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'dni')
    list_display = ('user', 'rol', 'dni', 'telefono')
