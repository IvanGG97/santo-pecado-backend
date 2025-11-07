from django.db import transaction
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Pedido, Estado_Pedido, Detalle_Pedido
from inventario.models import Producto_X_Insumo, Insumo
import re


def parsear_insumos_removidos(notas):
    """
    Helper para leer las notas (ej: "Hamburguesa (Sin: Tomate, Queso)")
    y devolver un set de insumos removidos (ej: {"tomate", "queso"}).
    """
    insumos_removidos = set()
    if not notas:
        return insumos_removidos

    # --- INICIO DE LA CORRECCIÓN ---

    # Regex para encontrar el bloque "Sin: [lista]"
    # Busca "Sin: " y captura todo lo que sigue (Grupo 1: .*?)
    # hasta que encuentra un pipe '|', un ')' o el final del string '$'
    match = re.search(r"Sin: (.*?)(?:\||\)|$)", notas, re.IGNORECASE)

    if match:
        # match.group(1) es la lista, ej: " Tomate, Queso "
        lista_insumos_sin = match.group(1).strip()

        # Dividimos la lista por comas
        nombres = lista_insumos_sin.split(",")

        for nombre in nombres:
            nombre_limpio = nombre.strip().lower()
            if nombre_limpio:  # Evitar strings vacíos
                insumos_removidos.add(nombre_limpio)

    # --- FIN DE LA CORRECCIÓN ---

    # Debug: Imprime qué insumos encontró para remover
    if insumos_removidos:
        print(f"INFO (Parser): Insumos a remover encontrados: {insumos_removidos}")

    return insumos_removidos


@receiver(pre_save, sender=Pedido)
def descontar_stock_en_preparacion(sender, instance, **kwargs):
    """
    Señal que se dispara antes de guardar un Pedido.
    Descuenta el stock de insumos si el estado cambia a "En Preparación".
    """
    if not instance.pk:
        return

    try:
        estado_en_preparacion = Estado_Pedido.objects.get(
            estado_pedido_nombre="En Preparación"
        )
    except Estado_Pedido.DoesNotExist:
        print(
            "ADVERTENCIA: El estado 'En Preparación' no existe. No se descontará stock."
        )
        return

    # --- La lógica se activa SOLO si el estado NUEVO es "En Preparación" ---
    if instance.estado_pedido_id != estado_en_preparacion.id:
        return

    try:
        pedido_anterior = Pedido.objects.get(pk=instance.pk)
    except Pedido.DoesNotExist:
        return

    # --- Evitar descuento múltiple si ya estaba "En Preparación" ---
    if pedido_anterior.estado_pedido_id == estado_en_preparacion.id:
        return

    print(
        f"INFO: Descontando stock para Pedido N°{instance.id} entrando a 'En Preparación'..."
    )

    try:
        with transaction.atomic():
            insumos_a_descontar = {}
            detalles = instance.detalles.all().select_related("producto")

            for detalle in detalles:
                if not detalle.producto:
                    continue

                insumos_removidos_nombres = parsear_insumos_removidos(detalle.notas)
                receta = Producto_X_Insumo.objects.filter(
                    producto=detalle.producto
                ).select_related("insumo")

                for item_receta in receta:
                    insumo = item_receta.insumo

                    if insumo.insumo_nombre.lower() not in insumos_removidos_nombres:
                        cantidad_requerida = (
                            item_receta.producto_insumo_cantidad * detalle.cantidad
                        )
                        insumo_id = insumo.id
                        insumos_a_descontar[insumo_id] = (
                            insumos_a_descontar.get(insumo_id, 0) + cantidad_requerida
                        )
                    else:
                        print(
                            f"INFO: Omitiendo descuento de '{insumo.insumo_nombre}' (removido en notas)."
                        )

            # 3. Verificar stock y descontar
            for insumo_id, cantidad_total in insumos_a_descontar.items():

                insumo = Insumo.objects.select_for_update().get(id=insumo_id)

                print(
                    f"Descontando: {cantidad_total} de '{insumo.insumo_nombre}'. Stock actual: {insumo.insumo_stock}"
                )

                if insumo.insumo_stock < cantidad_total:

                    # --- INICIO DE LA MODIFICACIÓN ---
                    # Mensaje de error personalizado como solicitaste
                    raise ValidationError(
                        f"El insumo '{insumo.insumo_nombre}' es insuficiente para este pedido."
                    )
                    # --- FIN DE LA MODIFICACIÓN ---

                insumo.insumo_stock = F("insumo_stock") - cantidad_total
                insumo.save()

            print(f"INFO: Stock descontado exitosamente para Pedido N°{instance.id}.")

    except ValidationError as e:
        # Capturar el error de stock insuficiente y relanzarlo
        raise e
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"ERROR: Error inesperado al descontar stock: {e}")
        raise ValidationError(
            f"Error al procesar el stock. Contacte al administrador. Detalles: {e}"
        )
