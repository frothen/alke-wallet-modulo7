"""Ejemplos para ejecutar dentro de: python manage.py shell"""
from django.db.models import Count, Sum, Q
from django.db import connection
from gestion.models import Cliente, Cuenta, Transaccion

# 1) Filtro: clientes con email de dominio example.com
clientes_demo = Cliente.objects.filter(email__iendswith="@example.com")
print("Clientes demo:", list(clientes_demo.values("id", "nombre", "email")))

# 2) Excluir cuentas cerradas
cuentas_activas = Cuenta.objects.exclude(estado="cerrada")
print("Cuentas no cerradas:", list(cuentas_activas.values("alias", "estado", "saldo")))

# 3) Anotación: cantidad de cuentas por cliente
clientes_con_cantidad = Cliente.objects.annotate(cantidad_cuentas=Count("cuentas"))
print("Cuentas por cliente:", list(clientes_con_cantidad.values("nombre", "cantidad_cuentas")))

# 4) Agregación: saldo agrupado por moneda
resumen = Cuenta.objects.values("moneda").annotate(total=Sum("saldo")).order_by("moneda")
print("Saldo por moneda (sin conversión):", list(resumen))

# 5) SQL parametrizado con cursor
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM gestion_cuenta WHERE estado = %s", ["activa"])
    print("Cuentas activas:", cursor.fetchone()[0])

# 6) raw() con parámetro. Los nombres de tabla/campos corresponden al modelo Cuenta.
cuentas_raw = Cuenta.objects.raw(
    "SELECT * FROM gestion_cuenta WHERE estado = %s ORDER BY saldo DESC", ["activa"]
)
print("Consulta raw:", [(c.alias, c.saldo) for c in cuentas_raw])
