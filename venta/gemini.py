import json
from http.client import HTTPException
from urllib.request import Request, urlopen

from django.conf import settings

GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'

PROMPT = """
Actúa como un experto consultor de negocios gastronómicos y data analyst.
Analiza los siguientes datos de mi restaurante "Santo Pecado" correspondientes al último periodo filtrado:

1. DATOS GENERALES:
- Ventas totales analizadas (cantidad de transacciones): {ventasTotales}

2. TOP PRODUCTOS MÁS VENDIDOS:
{topProductos}

3. INGRESOS POR DÍA (MEJORES DÍAS):
{topDias}

4. PREFERENCIA DE PAGO:
{mediosPago}

5. ALERTAS DE STOCK (CRÍTICO):
{stockBajo}

---
TAREA:
Genera un "Informe Estratégico de Desempeño".
El formato debe ser texto plano pero bien estructurado con los siguientes puntos:

1. **Resumen Ejecutivo**: Una visión general breve del estado del negocio.
2. **Análisis de Tendencias**: ¿Qué productos lideran? ¿Qué días son los más fuertes?
3. **Alertas de Inventario**: Recomendaciones urgentes sobre el stock bajo.
4. **3 Recomendaciones Estratégicas**: Acciones concretas para aumentar ventas o mejorar eficiencia basadas en estos datos.

Usa un tono profesional, motivador y directo. No uses formato Markdown (negritas, etc), usa texto plano para que pueda imprimirse en PDF fácilmente.
"""


class GeminiError(Exception):
    """Gemini no devolvió un reporte."""


def armar_prompt(datos):
    return PROMPT.format(
        ventasTotales=datos['ventasTotales'],
        topProductos=json.dumps(datos['topProductos'], ensure_ascii=False),
        topDias=json.dumps(datos['topDias'], ensure_ascii=False),
        mediosPago=json.dumps(datos['mediosPago'], ensure_ascii=False),
        stockBajo=json.dumps(datos['stockBajo'], ensure_ascii=False),
    )


def generar_reporte(datos):
    cuerpo = {'contents': [{'parts': [{'text': armar_prompt(datos)}]}]}
    pedido = Request(
        GEMINI_URL,
        data=json.dumps(cuerpo).encode('utf-8'),
        # La clave va en un encabezado para que no quede en los registros de URLs.
        headers={'Content-Type': 'application/json', 'x-goog-api-key': settings.GEMINI_API_KEY},
        method='POST',
    )
    try:
        with urlopen(pedido, timeout=60) as respuesta:
            resultado = json.load(respuesta)
        return resultado['candidates'][0]['content']['parts'][0]['text']
    except (OSError, HTTPException, ValueError, KeyError, IndexError, TypeError) as error:
        raise GeminiError(str(error)) from error
