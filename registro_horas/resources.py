from import_export import resources
from .models import Empleados

class EmpleadosResource(resources.ModelResource):
    class meta:
        model = Empleados