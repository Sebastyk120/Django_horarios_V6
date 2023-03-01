from django.forms import ModelForm
from .models import Empleados, Jornada


class CrearempleadoForm(ModelForm):
    class Meta:
        ordering = ['nombre']
        model = Empleados
        fields = ["nombre", "cedula", "estado", "empresa"]


class CrearjornadaForm(ModelForm):
    class Meta:
        model = Jornada
        fields = ["empleado", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global",
                  "salida_descanso_global", "inicio_descanso_global2", "salida_descanso_global2", "jornada_legal"]
