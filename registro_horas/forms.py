from django.forms import ModelForm
from django import forms
from .models import Empleados, Jornada, Cargos


class CrearempleadoForm(ModelForm):
    class Meta:
        ordering = ['nombre']
        model = Empleados
        widgets = {
            'ingreso': forms.TextInput(attrs={'type': 'date'}),
            'retiro': forms.TextInput(attrs={'type': 'date'}),
            
        }
        fields = ["nombre", "cedula", "empresa", "estado", "area",
                  "cargo", "salario", "generaextras", "ingreso", "retiro"]


class CrearjornadaForm(ModelForm):
    class Meta:
        model = Jornada
        widgets = {
            'inicio_jornada_global': forms.TextInput(attrs={'type': 'datetime-local'}),
            'salida_jornada_global': forms.TextInput(attrs={'type': 'datetime-local'}),
            'inicio_descanso_global': forms.TextInput(attrs={'type': 'datetime-local'}),
            'salida_descanso_global': forms.TextInput(attrs={'type': 'datetime-local'}),
            'inicio_descanso_global2': forms.TextInput(attrs={'type': 'datetime-local'}),
            'salida_descanso_global2': forms.TextInput(attrs={'type': 'datetime-local'}),
            
        }
        fields = ["empleado", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global",
                  "salida_descanso_global", "inicio_descanso_global2", "salida_descanso_global2", "jornada_legal"]


class CrearcargoForm(ModelForm):
    class Meta:
        model = Cargos
        fields = ["cargo"]
