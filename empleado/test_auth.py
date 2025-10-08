# test_auth.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Empleado, Rol, Empleado_x_rol

class AuthTestCase(TestCase):
    def setUp(self):
        self.rol = Rol.objects.create(rol_nombre="Cajero")
        
    def test_usuario_empleado_relation(self):
        # Crear usuario
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Verificar que se creó el empleado automáticamente
        self.assertTrue(hasattr(user, 'empleado'))
        self.assertEqual(user.empleado.empleado_nombre, 'Test')
        
    def test_login_api(self):
        # Crear usuario de prueba
        user = User.objects.create_user('testuser2', 'test@example.com', 'testpass123')
        
        # Probamos el login con el cliente de测试
        response = self.client.post('/api/login/', {
            'username': 'testuser2',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())