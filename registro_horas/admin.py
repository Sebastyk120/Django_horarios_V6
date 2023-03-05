from django.contrib import admin
from .models import Empleados, Jornada, Cargos


class JornadaAdmin(admin.ModelAdmin):
    readonly_fields = ("fh_transaccion",)


# Registrando Modelos de Heavens
admin.site.register(Empleados)
admin.site.register(Jornada, JornadaAdmin)
admin.site.register(Cargos)


