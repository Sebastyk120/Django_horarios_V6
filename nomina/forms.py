from datetime import datetime
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django import forms
from django.forms import ModelForm

from .models import Empleados, Jornada, Cargos, Festivos, OpeJornada


class CrearempleadoForm(ModelForm):
    class Meta:
        ordering = ['nombre']
        model = Empleados
        widgets = {
            'ingreso': forms.TextInput(attrs={'type': 'date'}),
            'retiro': forms.TextInput(attrs={'type': 'date'}),
            'nombre': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Ingrese El Nombre Completo'}),
            'cedula': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Ingrese Documento'}),
        }
        fields = ["nombre", "cedula", "tdoc", "empresa", "estado", "area", "contrato",
                  "cargo", "salario", "generaextras", "ingreso", "retiro"]

    def __init__(self, *args, **kwargs):
        super(CrearempleadoForm, self).__init__(*args, **kwargs)
        now = timezone.now()
        self.fields['ingreso'].widget.attrs['max'] = now.strftime('%Y-%m-%d')
        self.fields['retiro'].widget.attrs['max'] = now.strftime('%Y-%m-%d')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                Div('nombre', css_class='col-sm-6'),
                Div('cedula', css_class='col-sm-6'),
                Div('tdoc', css_class='col-sm-6'),
                Div('empresa', css_class='col-sm-6'),
                Div('estado', css_class='col-sm-6'),
                Div('area', css_class='col-sm-6'),
                css_class='row'
            ),
            Div(
                Div('contrato', css_class='col-sm-6'),
                Div('cargo', css_class='col-sm-6'),
                Div('salario', css_class='col-sm-6'),
                Div('generaextras', css_class='col-sm-6'),
                Div('ingreso', css_class='col-sm-6'),
                Div('retiro', css_class='col-sm-6'),
                css_class='row'
            ),
            Submit('submit', 'Guardar', css_class='d-grid gap-2 col-6 mx-auto')
        )


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

    def __init__(self, *args, **kwargs):
        super(CrearjornadaForm, self).__init__(*args, **kwargs)
        now = timezone.now()
        self.fields['inicio_jornada_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['salida_jornada_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global2'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global2'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_jornada_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['salida_jornada_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global2'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global2'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-6'
        self.helper.layout = Layout(
            Div(
                Div('inicio_jornada_global', css_class='col-sm-6'),
                Div('salida_jornada_global', css_class='col-sm-6'),
                Div('inicio_descanso_global', css_class='col-sm-6'),
                Div('salida_descanso_global', css_class='col-sm-6'),
                css_class='row'
            ),
            Div(
                Div('inicio_descanso_global2', css_class='col-sm-6'),
                Div('salida_descanso_global2', css_class='col-sm-6'),
                Div('jornada_legal', css_class='col-sm-6'),
                Div('empleado', css_class='col-sm-6'),
                css_class='row'
            ),
        )


class CrearcargoForm(ModelForm):
    class Meta:
        model = Cargos
        fields = ["cargo"]


class CrearfestivoForm(ModelForm):
    class Meta:
        model = Festivos
        widgets = {
            'festivo': forms.DateInput(attrs={'type': 'date'}),
        }
        fields = ["festivo"]


# --------------------------------------- OPERACIONES ----------------------------------------------------------------

class OpeCrearjornadaForm(ModelForm):
    class Meta:
        model = OpeJornada
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

    def __init__(self, *args, **kwargs):
        super(OpeCrearjornadaForm, self).__init__(*args, **kwargs)

        now = timezone.now()
        self.fields['inicio_jornada_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['salida_jornada_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global2'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global2'].widget.attrs['max'] = now.strftime('%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_jornada_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['salida_jornada_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['inicio_descanso_global2'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')
        self.fields['salida_descanso_global2'].widget.attrs['min'] = datetime(2023, 1, 1, 0, 0).strftime(
            '%Y-%m-%dT%H:%M:%S')

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-6'
        self.helper.layout = Layout(
            Div(
                Div('inicio_jornada_global', css_class='col-sm-6'),
                Div('salida_jornada_global', css_class='col-sm-6'),
                Div('inicio_descanso_global', css_class='col-sm-6'),
                Div('salida_descanso_global', css_class='col-sm-6'),
                css_class='row'
            ),
            Div(
                Div('inicio_descanso_global2', css_class='col-sm-6'),
                Div('salida_descanso_global2', css_class='col-sm-6'),
                Div('jornada_legal', css_class='col-sm-6'),
                Div('empleado', css_class='col-sm-6'),
                css_class='row'
            ),
        )
