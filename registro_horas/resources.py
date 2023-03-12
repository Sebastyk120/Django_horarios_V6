from import_export import resources
from .models import Empleados, Jornada, Cargos

class EmpleadosResource(resources.ModelResource):
    class Meta:
        model = Empleados
        

class JornadasResource(resources.ModelResource):
    class Meta:
        model = Jornada
        

class CargosResource(resources.ModelResource):
    class Meta:
        model = Cargos