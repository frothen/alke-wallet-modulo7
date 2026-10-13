from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ClienteForm, CuentaForm, TransaccionForm
from .models import Cliente, Cuenta, Transaccion


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "gestion/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cliente = Cliente.objects.filter(usuario=self.request.user).first()
        cuentas = Cuenta.objects.filter(cliente=cliente) if cliente else Cuenta.objects.none()
        ctx["cliente"] = cliente
        ctx["cuentas"] = cuentas
        ctx["total_cuentas"] = cuentas.count()
        ctx["saldo_total"] = cuentas.aggregate(total=Sum("saldo"))["total"] or 0
        ctx["transacciones_recientes"] = Transaccion.objects.filter(
            Q(cuenta_origen__cliente=cliente) | Q(cuenta_destino__cliente=cliente)
        ).select_related("cuenta_origen", "cuenta_destino")[:5] if cliente else Transaccion.objects.none()
        return ctx


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestion/formulario.html"
    success_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        if Cliente.objects.filter(usuario=request.user).exists():
            messages.info(request, "Tu usuario ya tiene un perfil de cliente.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Perfil de cliente creado.")
        return super().form_valid(form)


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "gestion/cliente_detalle.html"
    context_object_name = "cliente"

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestion/formulario.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class CuentaListView(LoginRequiredMixin, ListView):
    model = Cuenta
    template_name = "gestion/cuenta_lista.html"
    context_object_name = "cuentas"

    def get_queryset(self):
        return Cuenta.objects.filter(cliente__usuario=self.request.user).select_related("cliente")


class CuentaDetailView(LoginRequiredMixin, DetailView):
    model = Cuenta
    template_name = "gestion/cuenta_detalle.html"
    context_object_name = "cuenta"

    def get_queryset(self):
        return Cuenta.objects.filter(cliente__usuario=self.request.user).prefetch_related("beneficiarios")


class CuentaCreateView(LoginRequiredMixin, CreateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = "gestion/formulario.html"
    success_url = reverse_lazy("cuentas_lista")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["cliente"].queryset = Cliente.objects.filter(usuario=self.request.user)
        form.fields["beneficiarios"].queryset = Cliente.objects.exclude(usuario=self.request.user)
        return form

    def form_valid(self, form):
        if form.instance.cliente.usuario_id != self.request.user.id:
            form.add_error("cliente", "Solo puedes crear cuentas para tu propio perfil.")
            return self.form_invalid(form)
        messages.success(self.request, "Cuenta creada.")
        return super().form_valid(form)


class CuentaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cuenta
    form_class = CuentaForm
    template_name = "gestion/formulario.html"
    success_url = reverse_lazy("cuentas_lista")

    def get_queryset(self):
        return Cuenta.objects.filter(cliente__usuario=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["cliente"].queryset = Cliente.objects.filter(usuario=self.request.user)
        form.fields["beneficiarios"].queryset = Cliente.objects.exclude(usuario=self.request.user)
        return form

    def form_valid(self, form):
        if form.instance.cliente.usuario_id != self.request.user.id:
            form.add_error("cliente", "Solo puedes administrar tus propias cuentas.")
            return self.form_invalid(form)
        messages.success(self.request, "Cuenta actualizada.")
        return super().form_valid(form)


class CuentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cuenta
    template_name = "gestion/confirmar_eliminacion.html"
    success_url = reverse_lazy("cuentas_lista")

    def get_queryset(self):
        return Cuenta.objects.filter(cliente__usuario=self.request.user)


class TransaccionListView(LoginRequiredMixin, ListView):
    model = Transaccion
    template_name = "gestion/transaccion_lista.html"
    context_object_name = "transacciones"

    def get_queryset(self):
        return Transaccion.objects.filter(
            Q(cuenta_origen__cliente__usuario=self.request.user) |
            Q(cuenta_destino__cliente__usuario=self.request.user)
        ).select_related("cuenta_origen", "cuenta_destino")


class TransaccionCreateView(LoginRequiredMixin, CreateView):
    model = Transaccion
    form_class = TransaccionForm
    template_name = "gestion/formulario.html"
    success_url = reverse_lazy("transacciones_lista")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["cuenta_origen"].queryset = Cuenta.objects.filter(cliente__usuario=self.request.user)
        form.fields["cuenta_destino"].queryset = Cuenta.objects.all()
        return form

    def form_valid(self, form):
        origen = form.cleaned_data["cuenta_origen"]
        destino = form.cleaned_data["cuenta_destino"]
        if origen.cliente.usuario_id != self.request.user.id:
            form.add_error("cuenta_origen", "La cuenta de origen debe ser tuya.")
            return self.form_invalid(form)
        if destino.cliente.usuario_id == self.request.user.id:
            form.add_error("cuenta_destino", "Selecciona una cuenta de destino de otro cliente.")
            return self.form_invalid(form)
        # El módulo es académico: registra la transacción, no mueve dinero automáticamente.
        messages.success(self.request, "Transacción registrada. El registro no modifica saldos automáticamente.")
        return super().form_valid(form)


class TransaccionDetailView(LoginRequiredMixin, DetailView):
    model = Transaccion
    template_name = "gestion/transaccion_detalle.html"
    context_object_name = "transaccion"

    def get_queryset(self):
        return Transaccion.objects.filter(
            Q(cuenta_origen__cliente__usuario=self.request.user) |
            Q(cuenta_destino__cliente__usuario=self.request.user)
        ).select_related("cuenta_origen", "cuenta_destino")


class ReporteView(LoginRequiredMixin, TemplateView):
    template_name = "gestion/reporte.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = Cuenta.objects.filter(cliente__usuario=self.request.user)
        ctx["cuentas_por_moneda"] = qs.values("moneda").annotate(cantidad=Count("id"), saldo_total=Sum("saldo")).order_by("moneda")
        ctx["movimientos_por_estado"] = Transaccion.objects.filter(
            Q(cuenta_origen__cliente__usuario=self.request.user) |
            Q(cuenta_destino__cliente__usuario=self.request.user)
        ).values("estado").annotate(cantidad=Count("id"), monto_total=Sum("monto")).order_by("estado")
        return ctx
