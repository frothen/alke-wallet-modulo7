from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Cuenta, Transaccion


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono"]
        labels = {"nombre": "Nombre completo", "email": "Correo electrónico", "telefono": "Teléfono"}

    def clean_nombre(self):
        value = self.cleaned_data["nombre"].strip()
        if len(value) < 2:
            raise ValidationError("El nombre debe contener al menos 2 caracteres.")
        return value


class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ["cliente", "alias", "numero", "moneda", "tipo", "estado", "saldo", "beneficiarios"]
        labels = {"cliente": "Cliente", "alias": "Alias", "numero": "Número de cuenta",
                  "moneda": "Moneda", "tipo": "Tipo", "estado": "Estado", "saldo": "Saldo inicial",
                  "beneficiarios": "Beneficiarios guardados"}
        widgets = {"beneficiarios": forms.CheckboxSelectMultiple()}

    def clean_moneda(self):
        value = self.cleaned_data["moneda"].strip().upper()
        if len(value) != 3 or not value.isalpha():
            raise ValidationError("La moneda debe ser un código de tres letras, por ejemplo CLP.")
        return value


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["cuenta_origen", "cuenta_destino", "tipo", "estado", "monto", "descripcion"]
        labels = {"cuenta_origen": "Cuenta de origen", "cuenta_destino": "Cuenta de destino",
                  "tipo": "Tipo", "estado": "Estado", "monto": "Monto", "descripcion": "Descripción"}

    def clean(self):
        data = super().clean()
        origen = data.get("cuenta_origen")
        destino = data.get("cuenta_destino")
        monto = data.get("monto")
        if origen and destino and origen.pk == destino.pk:
            self.add_error("cuenta_destino", "La cuenta de origen y destino deben ser distintas.")
        if origen and destino and origen.moneda != destino.moneda:
            self.add_error("cuenta_destino", "Para esta versión, ambas cuentas deben usar la misma moneda.")
        if origen and monto and data.get("estado") == "confirmada" and origen.saldo < monto:
            self.add_error("monto", "La cuenta de origen no tiene saldo suficiente.")
        return data
