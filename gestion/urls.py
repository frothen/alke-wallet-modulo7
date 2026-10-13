from django.urls import path
from .views import (
    DashboardView, ClienteCreateView, ClienteDetailView, ClienteUpdateView,
    CuentaListView, CuentaDetailView, CuentaCreateView, CuentaUpdateView, CuentaDeleteView,
    TransaccionListView, TransaccionCreateView, TransaccionDetailView, ReporteView
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("perfil/nuevo/", ClienteCreateView.as_view(), name="cliente_crear"),
    path("perfil/<int:pk>/", ClienteDetailView.as_view(), name="cliente_detalle"),
    path("perfil/<int:pk>/editar/", ClienteUpdateView.as_view(), name="cliente_editar"),
    path("cuentas/", CuentaListView.as_view(), name="cuentas_lista"),
    path("cuentas/nueva/", CuentaCreateView.as_view(), name="cuenta_crear"),
    path("cuentas/<int:pk>/", CuentaDetailView.as_view(), name="cuenta_detalle"),
    path("cuentas/<int:pk>/editar/", CuentaUpdateView.as_view(), name="cuenta_editar"),
    path("cuentas/<int:pk>/eliminar/", CuentaDeleteView.as_view(), name="cuenta_eliminar"),
    path("transacciones/", TransaccionListView.as_view(), name="transacciones_lista"),
    path("transacciones/nueva/", TransaccionCreateView.as_view(), name="transaccion_crear"),
    path("transacciones/<int:pk>/", TransaccionDetailView.as_view(), name="transaccion_detalle"),
    path("reportes/", ReporteView.as_view(), name="reporte"),
]
