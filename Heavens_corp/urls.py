"""Heavens_corp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nomina import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('signup/', views.signup, name='signup'),
    path('jornadas/', views.jornadas, name='jornadas'),
    path('lista/jornadas/', views.list_jornadas, name='lista_jornadas'),
    path('jornadas/crear/', views.crear_jornada, name='crear_jornada'),
    path('jornadas/actualizar/<int:jornada_id>/', views.actualizar_jornada, name='actualizar_jornada'),
    path('jornadas/eliminar/<int:jornada_id>/', views.eliminar_jornada, name='eliminar_jornada'),
    path('jornadas/importar/', views.importar_excel_jor, name='import_jornada'),
    path('jornadas/exportar/', views.export_jor_excel, name='export_jornada'),
    path('empleados/', views.empleados, name='empleados'),
    path('lista/empleados/', views.list_empleados, name='lista_empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('festivos/crear/', views.crear_festivo, name='crear_festivo'),
    path('festivos/exportar/', views.export_festivos_excel, name='export_festivos'),
    path('festivos/importar/', views.importar_excel_festivos, name='importar_festivos'),
    path('empleados/importar/', views.importar_excel_emp, name='import_empleado'),
    path('empleados/exportar/', views.export_emp_excel, name='export_empleado'),
    path('cargos/importar/', views.importar_excel_cargo, name='import_cargo'),
    path('cargos/exportar/', views.export_cargos_excel, name='export_cargo'),
    path('cargos/crear/', views.crear_cargo, name='crear_cargo'),
    path('logout/', views.salir, name='logout'),
    # ------------------------------------------Operaciones--------------------------------------
    path('operaciones/', views.ope_home, name='ope_home'),
    path('ope_iniciar_sesion/', views.ope_iniciar_sesion, name='ope_iniciar_sesion'),
    path('operaciones/jornadas/', views.ope_jornadas, name='ope_jornadas'),
    path('operaciones/lista/jornadas/', views.ope_list_jornadas, name='ope_lista_jornadas'),
    path('operaciones/jornadas/crear/', views.ope_crear_jornada, name='ope_crear_jornada'),
    path('operaciones/jornadas/actualizar/<int:jornada_id>/', views.ope_actualizar_jornada, name='ope_actualizar_jornada'),
    path('operaciones/jornadas/eliminar/<int:jornada_id>/', views.ope_eliminar_jornada, name='ope_eliminar_jornada'),
    path('operaciones/jornadas/importar/', views.ope_importar_excel_jor, name='ope_import_jornada'),
    path('operaciones/jornadas/exportar/', views.ope_export_jor_excel, name='ope_export_jornada'),
    path('operaciones/empleados/', views.ope_empleados, name='ope_empleados'),
    path('operaciones/lista/empleados/', views.ope_list_empleados, name='ope_lista_empleados'),
    path('operaciones/festivos/ver/', views.ope_crear_festivo, name='ope_crear_festivo'),
    path('operaciones/cargos/ver/', views.ope_crear_cargo, name='ope_crear_cargo'),

]
