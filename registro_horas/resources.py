from import_export import resources, fields
from .models import Empleados, Jornada, Cargos, Festivos, OpeJornada


class EmpleadosResource(resources.ModelResource):
    class Meta:
        model = Empleados
        fields = ("id", "nombre", "cedula", "tdoc", "empresa", "estado", "area", "contrato",
                  "cargo", "salario", "generaextras", "ingreso", "retiro")

    def dehydrate_cargo(self, cargos):
        return cargos.cargo.cargo


class JornadasResource(resources.ModelResource):
    user = fields.Field(attribute='user__username', column_name='User')

    class Meta:
        model = Jornada
        fields = (
            "id", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global", "salida_descanso_global",
            "inicio_descanso_global2", "salida_descanso_global2",
            "jornada_legal", "empleado", "user", "total_horas", "diurnas_totales", "nocturnas_totales",
            "extras_diurnas_totales", "extras_nocturnos_totales",
            "diurnos_festivo_totales", "nocturnos_festivo_totales", "extras_diurnos_festivo_totales",
            "extras_nocturnos_festivo_totales")
        export_order = (
            "id", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global", "salida_descanso_global",
            "inicio_descanso_global2", "salida_descanso_global2",
            "jornada_legal", "empleado", "user", "total_horas", "diurnas_totales", "nocturnas_totales",
            "extras_diurnas_totales", "extras_nocturnos_totales",
            "diurnos_festivo_totales", "nocturnos_festivo_totales", "extras_diurnos_festivo_totales",
            "extras_nocturnos_festivo_totales")

    def dehydrate_empleado(self, empleados):
        return empleados.empleado.nombre


class CargosResource(resources.ModelResource):
    class Meta:
        model = Cargos


class FestivosResourse(resources.ModelResource):
    class Meta:
        model = Festivos


# -----------------------------------------OPERACIONES---------------------------------------------------------------

class OpeJornadasResource(resources.ModelResource):
    user = fields.Field(attribute='user__username', column_name='User')

    class Meta:
        model = OpeJornada
        fields = (
            "id", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global", "salida_descanso_global",
            "inicio_descanso_global2", "salida_descanso_global2",
            "jornada_legal", "empleado", "user", "total_horas", "diurnas_totales", "nocturnas_totales",
            "extras_diurnas_totales", "extras_nocturnos_totales",
            "diurnos_festivo_totales", "nocturnos_festivo_totales", "extras_diurnos_festivo_totales",
            "extras_nocturnos_festivo_totales")
        export_order = (
            "id", "inicio_jornada_global", "salida_jornada_global", "inicio_descanso_global", "salida_descanso_global",
            "inicio_descanso_global2", "salida_descanso_global2",
            "jornada_legal", "empleado", "user", "total_horas", "diurnas_totales", "nocturnas_totales",
            "extras_diurnas_totales", "extras_nocturnos_totales",
            "diurnos_festivo_totales", "nocturnos_festivo_totales", "extras_diurnos_festivo_totales",
            "extras_nocturnos_festivo_totales")

    def dehydrate_empleado(self, empleados):
        return empleados.empleado.nombre
