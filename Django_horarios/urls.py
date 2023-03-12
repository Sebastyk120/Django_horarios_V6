"""Django_horarios URL Configuration

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
from registro_horas import views

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
    path('empleados/', views.empleados, name='empleados'),
    path('lista/empleados/', views.list_empleados, name='lista_empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleados/importar/', views.importar_excel_emp, name='import_empleado'),
    path('cargos/importar/', views.importar_excel_cargo, name='import_cargo'),
    path('logout/', views.salir, name='logout'),   
    
]
