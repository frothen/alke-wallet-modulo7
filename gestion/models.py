from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse


class Cliente(models.Model):
    """Perfil de wallet asociado uno a uno con el usuario autenticado."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_wallet"
    )
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=20, blank=True,
        validators=[RegexValidator(r"^[0-9+() -]*$", "Usa solo números y símbolos telefónicos habituales.")]
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    TIPOS = [("personal", "Personal"), ("ahorro", "Ahorro"), ("empresa", "Empresa")]
    ESTADOS = [("activa", "Activa"), ("bloqueada", "Bloqueada"), ("cerrada", "Cerrada")]
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="cuentas")
    alias = models.CharField(max_length=80)
    numero = models.CharField(max_length=24, unique=True)
    moneda = models.CharField(max_length=3, default="CLP")
    tipo = models.CharField(max_length=12, choices=TIPOS, default="personal")
    estado = models.CharField(max_length=12, choices=ESTADOS, default="activa")
    saldo = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"),
                                validators=[MinValueValidator(Decimal("0.00"))])
    beneficiarios = models.ManyToManyField(
        Cliente, blank=True, related_name="cuentas_como_beneficiario",
        help_text="Clientes guardados como beneficiarios frecuentes."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["alias"]
        constraints = [
            models.CheckConstraint(condition=models.Q(saldo__gte=0), name="cuenta_saldo_no_negativo")
        ]

    def __str__(self):
        return f"{self.alias} ({self.numero})"

    def get_absolute_url(self):
        return reverse("cuenta_detalle", kwargs={"pk": self.pk})


class Transaccion(models.Model):
    TIPOS = [("transferencia", "Transferencia"), ("abono", "Abono"), ("cargo", "Cargo")]
    ESTADOS = [("pendiente", "Pendiente"), ("confirmada", "Confirmada"), ("rechazada", "Rechazada")]
    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="transacciones_enviadas")
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="transacciones_recibidas")
    tipo = models.CharField(max_length=20, choices=TIPOS, default="transferencia")
    estado = models.CharField(max_length=12, choices=ESTADOS, default="pendiente")
    monto = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    descripcion = models.CharField(max_length=180, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
        constraints = [
            models.CheckConstraint(condition=~models.Q(cuenta_origen=models.F("cuenta_destino")),
                                   name="transaccion_cuentas_distintas"),
            models.CheckConstraint(condition=models.Q(monto__gt=0), name="transaccion_monto_positivo"),
        ]

    def __str__(self):
        return f"Transacción #{self.pk} · {self.monto} {self.cuenta_origen.moneda}"
