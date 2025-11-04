from rest_framework import serializers
from .models import Producto, Tipo_Producto, Categoria_Insumo, Insumo, Producto_X_Insumo
import json


# --- Serializers de Lectura (actualizados) ---
class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Producto
        fields = ["id", "tipo_producto_nombre"]


# --- SERIALIZER DE INSUMO EN RECETA (CORREGIDO) ---
class InsumoEnRecetaSerializer(serializers.ModelSerializer):
    # Añadimos el campo de imagen para que la URL se genere correctamente
    insumo_imagen = serializers.ImageField(
        max_length=None, use_url=True, read_only=True
    )

    class Meta:
        model = Insumo
        # Añadimos los campos de imagen a la lista de fields
        fields = [
            "id",
            "insumo_nombre",
            "insumo_unidad",
            "insumo_imagen",
            "insumo_imagen_url",
        ]


# Nuevo serializer para leer la relación Producto <-> Insumo
class ProductoXInsumoReadSerializer(serializers.ModelSerializer):
    insumo = InsumoEnRecetaSerializer()  # Ahora usa el serializer corregido

    class Meta:
        model = Producto_X_Insumo
        fields = ["insumo", "producto_insumo_cantidad"]


class ProductoSerializer(serializers.ModelSerializer):
    tipo_producto = serializers.StringRelatedField()
    # --- ¡CAMPO AÑADIDO! ---
    # Necesitamos el ID para que el frontend pueda filtrar
    tipo_producto_id = serializers.PrimaryKeyRelatedField(
        source="tipo_producto", read_only=True
    )

    producto_imagen = serializers.ImageField(
        max_length=None, use_url=True, read_only=True
    )
    receta = ProductoXInsumoReadSerializer(
        many=True, source="producto_x_insumo_set", read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            "id",
            "producto_nombre",
            "producto_descripcion",
            "producto_precio",
            "producto_disponible",
            "producto_imagen",
            "producto_imagen_url",
            "tipo_producto",
            "tipo_producto_id",
            "receta",  # Campos añadidos
            "producto_fecha_hora_creacion",
        ]


# --- Serializer de Escritura (actualizado) ---


# Nuevo serializer para validar la receta que se envía
class RecetaWriteSerializer(serializers.Serializer):
    insumo_id = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=3)


class ProductoWriteSerializer(serializers.ModelSerializer):
    producto_imagen = serializers.ImageField(
        max_length=None, use_url=True, required=False, allow_null=True
    )
    # Añadimos el campo receta para la escritura
    receta = RecetaWriteSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Producto
        fields = [
            "tipo_producto",
            "producto_nombre",
            "producto_descripcion",
            "producto_precio",
            "producto_disponible",
            "producto_imagen",
            "producto_imagen_url",
            "receta",
        ]

    def to_internal_value(self, data):
        mutable_data = data.copy()
        for field_name in [
            "producto_imagen",
            "producto_imagen_url",
            "producto_descripcion",
        ]:
            if (
                field_name in mutable_data
                and isinstance(mutable_data[field_name], str)
                and not mutable_data[field_name]
            ):
                mutable_data[field_name] = None

        disponible = mutable_data.get("producto_disponible")
        if isinstance(disponible, str):
            mutable_data["producto_disponible"] = disponible.lower() in ("true", "on")

        tipo = mutable_data.get("tipo_producto")
        if isinstance(tipo, str) and tipo.isdigit():
            mutable_data["tipo_producto"] = int(tipo)

        # --- Convertimos la receta de JSON string a lista si viene de FormData ---
        receta_str = mutable_data.get("receta")
        if isinstance(receta_str, str):
            try:
                mutable_data["receta"] = json.loads(receta_str)
            except json.JSONDecodeError:
                pass

        return super().to_internal_value(mutable_data)

    def _guardar_receta(self, producto, receta_data):
        """Método auxiliar para crear las relaciones de la receta."""
        producto.producto_x_insumo_set.all().delete()  # Borramos la receta antigua
        for item in receta_data:
            insumo = Insumo.objects.get(id=item["insumo_id"])
            Producto_X_Insumo.objects.create(
                producto=producto,
                insumo=insumo,
                producto_insumo_cantidad=item["cantidad"],
            )

    def create(self, validated_data):
        receta_data = validated_data.pop("receta", [])

        if "producto_imagen" in validated_data and validated_data.get(
            "producto_imagen"
        ):
            validated_data["producto_imagen_url"] = None
        elif "producto_imagen_url" in validated_data and validated_data.get(
            "producto_imagen_url"
        ):
            validated_data["producto_imagen"] = None

        producto = super().create(validated_data)
        self._guardar_receta(producto, receta_data)  # Guardamos la receta
        return producto

    def update(self, instance, validated_data):
        receta_data = validated_data.pop("receta", None)

        if (
            "producto_imagen" in validated_data
            and validated_data.get("producto_imagen") is not None
        ):
            validated_data["producto_imagen_url"] = None
            instance.producto_imagen.delete(save=False)
        elif (
            "producto_imagen_url" in validated_data
            and validated_data.get("producto_imagen_url") is not None
        ):
            validated_data["producto_imagen"] = None
            instance.producto_imagen.delete(save=False)
        elif (
            validated_data.get("producto_imagen") is None
            and validated_data.get("producto_imagen_url") is None
        ):
            if (
                "producto_imagen" in validated_data
                or "producto_imagen_url" in validated_data
            ):
                instance.producto_imagen.delete(save=False)
                instance.producto_imagen_url = None

        producto = super().update(instance, validated_data)

        if receta_data is not None:  # Solo actualiza la receta si se envió data
            self._guardar_receta(producto, receta_data)

        return producto


# --- Serializers de Insumo (Corregidos) ---
class CategoriaInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria_Insumo
        fields = ["id", "categoria_insumo_nombre"]


class InsumoReadSerializer(serializers.ModelSerializer):
    categoria_insumo = serializers.StringRelatedField()
    insumo_imagen = serializers.ImageField(
        max_length=None, use_url=True, read_only=True
    )

    class Meta:
        model = Insumo
        fields = [
            "id",
            "categoria_insumo",
            "insumo_nombre",
            "insumo_unidad",
            "insumo_stock",
            "insumo_stock_minimo",
            "insumo_imagen",
            "insumo_imagen_url",
        ]


class InsumoWriteSerializer(serializers.ModelSerializer):
    insumo_imagen = serializers.ImageField(
        max_length=None, use_url=True, required=False, allow_null=True
    )

    class Meta:
        model = Insumo
        fields = [
            "categoria_insumo",
            "insumo_nombre",
            "insumo_unidad",
            "insumo_stock",
            "insumo_stock_minimo",
            "insumo_imagen",
            "insumo_imagen_url",
        ]

    def to_internal_value(self, data):
        mutable_data = data.copy()
        for field_name in ["insumo_imagen", "insumo_imagen_url"]:
            if (
                field_name in mutable_data
                and isinstance(mutable_data[field_name], str)
                and not mutable_data[field_name]
            ):
                mutable_data[field_name] = None
        categoria = mutable_data.get("categoria_insumo")
        if isinstance(categoria, str) and categoria.isdigit():
            mutable_data["categoria_insumo"] = int(categoria)
        return super().to_internal_value(mutable_data)

    def create(self, validated_data):
        if "insumo_imagen" in validated_data and validated_data.get("insumo_imagen"):
            validated_data["insumo_imagen_url"] = None
        elif "insumo_imagen_url" in validated_data and validated_data.get(
            "insumo_imagen_url"
        ):
            validated_data["insumo_imagen"] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if (
            "insumo_imagen" in validated_data
            and validated_data.get("insumo_imagen") is not None
        ):
            validated_data["insumo_imagen_url"] = None
            instance.insumo_imagen.delete(save=False)
        elif (
            "insumo_imagen_url" in validated_data
            and validated_data.get("insumo_imagen_url") is not None
        ):
            validated_data["insumo_imagen"] = None
            instance.insumo_imagen.delete(save=False)
        elif (
            validated_data.get("insumo_imagen") is None
            and validated_data.get("insumo_imagen_url") is None
        ):
            if (
                "insumo_imagen" in validated_data
                or "insumo_imagen_url" in validated_data
            ):
                instance.insumo_imagen.delete(save=False)
                instance.insumo_imagen_url = None
        return super().update(instance, validated_data)
