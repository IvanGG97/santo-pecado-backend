import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

CLAVE = 'clave-de-prueba'
DATOS = {
    'ventasTotales': 12,
    'topProductos': ['Hamburguesa (8u)'],
    'topDias': ['2025-11-01: $5000'],
    'mediosPago': ['Efectivo: $5000'],
    'stockBajo': ['Pan (Stock: 2)'],
}


class GeminiFalso(BaseHTTPRequestHandler):
    """Servidor local que responde como Gemini, para probar la llamada HTTP real."""
    estado = 200
    respuesta = {'candidates': [{'content': {'parts': [{'text': 'Informe de prueba'}]}}]}
    pedidos = []

    def do_POST(self):
        cuerpo = self.rfile.read(int(self.headers['Content-Length']))
        GeminiFalso.pedidos.append({'path': self.path, 'clave': self.headers['x-goog-api-key'], 'cuerpo': json.loads(cuerpo)})
        contenido = json.dumps(GeminiFalso.respuesta).encode('utf-8')
        self.send_response(GeminiFalso.estado)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def log_message(self, *args):
        pass


@override_settings(GEMINI_API_KEY=CLAVE)
class ReporteIATestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.servidor = ThreadingHTTPServer(('127.0.0.1', 0), GeminiFalso)
        Thread(target=cls.servidor.serve_forever, daemon=True).start()
        cls.url_gemini = f'http://127.0.0.1:{cls.servidor.server_port}/gemini'

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.servidor.server_close()
        super().tearDownClass()

    def setUp(self):
        cache.clear()
        GeminiFalso.estado = 200
        GeminiFalso.respuesta = {'candidates': [{'content': {'parts': [{'text': 'Informe de prueba'}]}}]}
        GeminiFalso.pedidos = []
        self.url = reverse('reporte-ia')
        apuntar = patch('venta.gemini.GEMINI_URL', self.url_gemini)
        apuntar.start()
        self.addCleanup(apuntar.stop)

    def autenticar(self, rol):
        usuario = User.objects.create_user(username=f'usuario-{rol}', password='clave-test')
        usuario.groups.add(Group.objects.create(name=rol))
        self.client.force_authenticate(user=usuario)

    def test_genera_el_reporte_para_los_roles_del_dashboard(self):
        for rol in ['Admin', 'Encargado/Cajero']:
            with self.subTest(rol=rol):
                self.autenticar(rol)
                respuesta = self.client.post(self.url, DATOS, format='json')
                self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
                self.assertEqual(respuesta.data, {'reporte': 'Informe de prueba'})

    def test_la_clave_va_en_el_encabezado_y_los_datos_en_el_prompt(self):
        self.autenticar('Admin')
        self.client.post(self.url, DATOS, format='json')
        pedido = GeminiFalso.pedidos[0]
        self.assertEqual(pedido['clave'], CLAVE)
        self.assertNotIn(CLAVE, pedido['path'])
        prompt = pedido['cuerpo']['contents'][0]['parts'][0]['text']
        for dato in ['12', 'Hamburguesa (8u)', '2025-11-01: $5000', 'Efectivo: $5000', 'Pan (Stock: 2)']:
            self.assertIn(dato, prompt)

    def test_rechaza_a_quien_no_inicio_sesion(self):
        respuesta = self.client.post(self.url, DATOS, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(GeminiFalso.pedidos, [])

    def test_rechaza_a_los_roles_sin_dashboard(self):
        for rol in ['Cocina', 'Cliente']:
            with self.subTest(rol=rol):
                self.autenticar(rol)
                respuesta = self.client.post(self.url, DATOS, format='json')
                self.assertEqual(respuesta.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(GeminiFalso.pedidos, [])

    def test_rechaza_datos_invalidos_sin_llamar_a_gemini(self):
        self.autenticar('Admin')
        invalidos = [
            {},
            {**DATOS, 'ventasTotales': -1},
            {**DATOS, 'topProductos': 'no es una lista'},
            {**DATOS, 'topProductos': ['x'] * 51},
            {**DATOS, 'stockBajo': ['x' * 201]},
        ]
        for datos in invalidos:
            respuesta = self.client.post(self.url, datos, format='json')
            self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(GeminiFalso.pedidos, [])

    def test_acepta_un_periodo_sin_datos(self):
        self.autenticar('Admin')
        vacio = {'ventasTotales': 0, 'topProductos': [], 'topDias': [], 'mediosPago': [], 'stockBajo': []}
        respuesta = self.client.post(self.url, vacio, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)

    @override_settings(GEMINI_API_KEY='')
    def test_sin_clave_configurada_no_llama_a_gemini(self):
        self.autenticar('Admin')
        respuesta = self.client.post(self.url, DATOS, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(GeminiFalso.pedidos, [])

    def test_un_error_de_gemini_no_expone_detalles(self):
        self.autenticar('Admin')
        GeminiFalso.estado = 403
        GeminiFalso.respuesta = {'error': {'message': f'API key not valid: {CLAVE}'}}
        with self.assertLogs('venta.views', level='ERROR'):
            respuesta = self.client.post(self.url, DATOS, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertEqual(respuesta.data, {'detail': 'No se pudo generar el reporte.'})

    def test_una_respuesta_sin_contenido_es_un_error(self):
        self.autenticar('Admin')
        GeminiFalso.respuesta = {'candidates': []}
        with self.assertLogs('venta.views', level='ERROR'):
            respuesta = self.client.post(self.url, DATOS, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_limita_los_reportes_por_hora(self):
        self.autenticar('Admin')
        for _ in range(10):
            self.assertEqual(self.client.post(self.url, DATOS, format='json').status_code, status.HTTP_200_OK)
        respuesta = self.client.post(self.url, DATOS, format='json')
        self.assertEqual(respuesta.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(len(GeminiFalso.pedidos), 10)
