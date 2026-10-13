from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Cliente, Cuenta, Transaccion


class AlkeWalletTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="ClaveSegura123!")
        self.other_user = User.objects.create_user(username="bruno", password="ClaveSegura123!")
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Ana Pérez", email="ana@example.com")
        self.otro = Cliente.objects.create(usuario=self.other_user, nombre="Bruno Díaz", email="bruno@example.com")
        self.cuenta = Cuenta.objects.create(cliente=self.cliente, alias="Cuenta principal", numero="AW-0001", saldo=Decimal("10000"))
        self.cuenta_otro = Cuenta.objects.create(cliente=self.otro, alias="Cuenta Bruno", numero="AW-0002", saldo=Decimal("5000"))

    def test_one_to_one_cliente_usuario(self):
        self.assertEqual(self.user.perfil_wallet, self.cliente)

    def test_foreign_key_cuenta_cliente(self):
        self.assertEqual(self.cliente.cuentas.count(), 1)

    def test_many_to_many_beneficiarios(self):
        self.cuenta.beneficiarios.add(self.otro)
        self.assertIn(self.otro, self.cuenta.beneficiarios.all())

    def test_transaccion_registra_relaciones(self):
        t = Transaccion.objects.create(cuenta_origen=self.cuenta, cuenta_destino=self.cuenta_otro,
                                       monto=Decimal("500"), estado="pendiente")
        self.assertEqual(t.cuenta_origen, self.cuenta)

    def test_dashboard_requiere_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_usuario_no_ve_cuentas_ajenas(self):
        self.client.login(username="ana", password="ClaveSegura123!")
        response = self.client.get(reverse("cuentas_lista"))
        self.assertContains(response, "Cuenta principal")
        self.assertNotContains(response, "Cuenta Bruno")

    def test_formulario_protegido_csrf_en_template(self):
        self.client.login(username="ana", password="ClaveSegura123!")
        response = self.client.get(reverse("cliente_crear"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")
