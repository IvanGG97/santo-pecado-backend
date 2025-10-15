from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

# Create your tests here.
from empleado.models import Empleado, Rol, Empleado_x_rol
from cliente.models import Cliente
from caja.models import Caja
from inventario.models import Producto, Tipo_Producto
from .models import Estado_Venta

class VentaAPITestCase(APITestCase):
    """
    Tests para el endpoint de Ventas.
    """

    def setUp(self):
        """
        Configuración inicial para cada test.
        Crea los objetos necesarios en la base de datos de prueba.
        """
        # 1. Crear usuario y empleado para autenticación
        self.user = User.objects.create_user(username='testuser', password='testpassword', first_name='Test', last_name='User')
        self.empleado = Empleado.objects.create(user=self.user)
        self.rol = Rol.objects.create(rol_nombre='Vendedor')
        self.empleado_rol = Empleado_x_rol.objects.create(empleado=self.empleado, rol=self.rol)

        # 2. Crear datos necesarios para una venta
        self.cliente = Cliente.objects.create(cliente_nombre='John', cliente_apellido='Doe', cliente_telefono='123456789')
        self.caja = Caja.objects.create(empleado_x_rol=self.empleado_rol, caja_monto_inicial=1000, caja_estado=True)
        self.estado_venta = Estado_Venta.objects.create(estado_venta_nombre='Completada')
        self.tipo_producto = Tipo_Producto.objects.create(tipo_producto_nombre='Bebida')
        self.producto = Producto.objects.create(
            tipo_producto=self.tipo_producto, 
            producto_nombre='Café', 
            producto_precio=150.00
        )

        # 3. Autenticar el cliente de prueba
        self.client.force_authenticate(user=self.user)

    def test_crear_venta(self):
        """
        Prueba que se pueda crear una nueva venta correctamente.
        """
        # URL para crear ventas
        url = reverse('venta-list') # 'venta-list' es el nombre que el router le da a la URL de /api/venta/ventas/

        # Datos para la nueva venta
        data = {
            "cliente": self.cliente.id,
            "empleado_x_rol": self.empleado_rol.id,
            "caja": self.caja.id,
            "estado_venta": self.estado_venta.id,
            "venta_medio_pago": "efectivo",
            "detalles_write": [
                {
                    "producto_id": self.producto.id,
                    "cantidad": 2
                }
            ]
        }

        # Realizar la petición POST
        response = self.client.post(url, data, format='json')

        # 1. Verificar que la respuesta sea 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. Verificar que el total de la venta se haya calculado correctamente
        self.assertEqual(response.data['venta_total'], '300.00') # 2 * 150.00

        # 3. Verificar que el producto vendido esté en los detalles
        self.assertEqual(response.data['detalles'][0]['item_nombre'], 'Café')
