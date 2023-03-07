from django.forms import ModelForm
from django import forms
from .models import Empleados, Jornada, Cargos
from datetime import datetime, timedelta


class CrearempleadoForm(ModelForm):
    class Meta:
        ordering = ['nombre']
        model = Empleados
        widgets = {
            'ingreso': forms.TextInput(attrs={'type': 'date', 'max': datetime.now().date}),
            'retiro': forms.TextInput(attrs={'type': 'date', 'max': datetime.now().date}),
            'nombre': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Ingrese el nombre'}),
            'cedula': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Ingrese Documento'}),
        }
        fields = ["nombre", "cedula", "empresa", "estado", "area",
                  "cargo", "salario", "generaextras", "ingreso", "retiro"]


iniciop = datetime.now()
inicio = datetime.strftime(iniciop, "%Y-%m-%dT%H:%M:%S")


class CrearjornadaForm(ModelForm):
    class Meta:
        model = Jornada
        widgets = {
            'inicio_jornada_global': forms.TextInput(attrs={'type': 'datetime-local', 'max': inicio}),
            'salida_jornada_global': forms.TextInput(attrs={'type': 'datetime-local', 'max': inicio}),
            'inicio_descanso_global': forms.TextInput(attrs={'type': 'datetime-local', 'max': inicio}),
            'salida_descanso_global': forms.TextInput(attrs={'type': 'datetime-local', 'max': inicio}),
            'inicio_descanso_global2': forms.TextInput(attrs={'type': 'datetime-local', 'max': inicio}),
            'salida_descanso_global2': forms.TextInput(attrs={'type': 'datetime-local', 'max': inicio}),

        }
        fields = ["empleado", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global",
                  "salida_descanso_global", "inicio_descanso_global2", "salida_descanso_global2", "jornada_legal"]


class CrearcargoForm(ModelForm):
    class Meta:
        model = Cargos
        fields = ["cargo"]
