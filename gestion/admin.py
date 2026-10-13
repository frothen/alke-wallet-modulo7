from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "email", "telefono", "usuario", "fecha_creacion")
    search_fields = ("nombre", "email", "usuario__username")
    list_filter = ("fecha_creacion",)


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("id", "alias", "numero", "cliente", "moneda", "saldo", "estado")
    search_fields = ("alias", "numero", "cliente__nombre", "cliente__email")
    list_filter = ("moneda", "tipo", "estado")
    filter_horizontal = ("beneficiarios",)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("id", "cuenta_origen", "cuenta_destino", "tipo", "monto", "estado", "fecha")
    search_fields = ("descripcion", "cuenta_origen__numero", "cuenta_destino__numero")
    list_filter = ("tipo", "estado", "fecha")
    readonly_fields = ("fecha",)
