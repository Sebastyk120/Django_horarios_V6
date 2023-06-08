from datetime import timedelta, datetime
from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from tablib import Dataset
from .calc_horarios import Horarios
from .forms import CrearjornadaForm, CrearempleadoForm, CrearfestivoForm, CrearcargoForm, OpeCrearjornadaForm
from .models import Jornada, Empleados, Cargos, Festivos, OpeJornada
from .resources import EmpleadosResource, JornadasResource, CargosResource, FestivosResourse, OpeJornadasResource


# Create your views here.

def home(request):
    if request.user.username == 'asanchez':
        return redirect('ope_home')
    elif request.user.username == 'mbonilla':
        return redirect('ope_home')
    else:
        return render(request, 'home.html')


def export_emp_excel(request):
    empleados_resource = EmpleadosResource()
    dataset = empleados_resource.export()
    response = HttpResponse(dataset.xls,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="empleados_exportados.xls"'
    return response


def export_jor_excel(request):
    jornada_resource = JornadasResource()
    dataset = jornada_resource.export()
    response = HttpResponse(dataset.xls,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="jornadas_exportados.xls"'
    return response


def export_cargos_excel(request):
    cargos_resource = CargosResource()
    dataset = cargos_resource.export()
    response = HttpResponse(dataset.xls,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="cargos_exportados.xls"'
    return response


def export_festivos_excel(request):
    festivos_resource = FestivosResourse()
    dataset = festivos_resource.export()
    response = HttpResponse(dataset.xls,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="festivos_exportados.xls"'
    return response


def importar_excel_emp(request):
    if request.method == 'POST':
        empleados_resource = EmpleadosResource()
        dataset = Dataset()
        new_empleados = request.FILES['empleados']
        imported_data = dataset.load(new_empleados.read(), format='xlsx')
        for data in imported_data:
            valor = Empleados(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
            )
            valor.save()
            messages.success(
                request, "Excel de empleados importado correctamente")
    return render(request, 'import_empleados.html')


def importar_excel_jor(request):
    if request.method == 'POST':
        jornadas_resource = JornadasResource()
        dataset = Dataset()
        new_jornada = request.FILES['jornadas']
        imported_data = dataset.load(new_jornada.read(), format='xlsx')
        for data in imported_data:
            horarioo = Horarios(data[1], data[2], data[3],
                                data[4], data[5], data[6], data[7])
            valor = Jornada(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                user=request.user,
                total_horas=horarioo.total_horas,
                diurnas_totales=horarioo.diurnas_totales,
                nocturnas_totales=horarioo.nocturnas_totales,
                extras_diurnas_totales=horarioo.extras_diurnas_totales,
                extras_nocturnos_totales=horarioo.extras_nocturnos_totales,
                diurnos_festivo_totales=horarioo.diurnos_festivo_totales,
                nocturnos_festivo_totales=horarioo.nocturnos_festivo_totales,
                extras_diurnos_festivo_totales=horarioo.extras_diurnos_festivo_totales,
                extras_nocturnos_festivo_totales=horarioo.extras_nocturnos_festivo_totales,
            )
            valor.save()
            messages.success(
                request, "Excel de jornadas importado correctamente")
    return render(request, 'import_jornadas.html')


def importar_excel_cargo(request):
    if request.method == 'POST':
        cargos_resource = CargosResource()
        dataset = Dataset()
        new_cargos = request.FILES['cargos']
        imported_data = dataset.load(new_cargos.read(), format='xlsx')
        for data in imported_data:
            valor = Cargos(
                data[0],
                data[1],
            )
            valor.save()
            messages.success(
                request, "Excel de cargos importado correctamente")
    return render(request, 'import_cargos.html')


def importar_excel_festivos(request):
    if request.method == 'POST':
        festivos_resource = FestivosResourse()
        dataset = Dataset()
        new_festivos = request.FILES['festivos']
        imported_data = dataset.load(new_festivos.read(), format='xlsx')
        for data in imported_data:
            valor = Festivos(
                data[0],
                data[1],
            )
            valor.save()
            messages.success(
                request, "Excel de festivos importado correctamente")
    return render(request, 'import_festivos.html')


def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar_sesion.html',
                          {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecto'})
        else:
            login(request, user)
            if user.username == 'prueba':
                return redirect('ope_home')
            else:
                return redirect('home')


@user_passes_test(lambda u: u.is_superuser)
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario.
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                messages.success(request, "usuario creado correctamente")
                login(request, user)
                return redirect('jornadas')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, "error": 'El usuario ya existe'})
        return render(request, 'signup.html', {'form': UserCreationForm, "error": 'Las contraseñas no coinciden'})


@permission_required('nomina.view_jornada', raise_exception=True)
@login_required
def jornadas(request):
    return render(request, 'jornadas.html')


@permission_required('nomina.view_jornada', raise_exception=True)
@login_required
def crear_jornada(request):
    if request.method == 'GET':
        return render(request, 'crear_jornada.html', {'form': CrearjornadaForm})
    else:
        try:
            form = CrearjornadaForm(request.POST)
            if request.user.has_perm('nomina.add_jornada'):
                if form.is_valid():
                    inicio_jornada_globalf = form.cleaned_data['inicio_jornada_global']
                    salida_jornada_globalf = form.cleaned_data['salida_jornada_global']
                    inicio_descanso_globalf = form.cleaned_data['inicio_descanso_global']
                    salida_descanso_globalf = form.cleaned_data['salida_descanso_global']
                    inicio_descanso_global2f = form.cleaned_data['inicio_descanso_global2']
                    salida_descanso_global2f = form.cleaned_data['salida_descanso_global2']
                    sumador_dia = inicio_jornada_globalf + timedelta(days=1)
                    sumador_dia2 = int(sumador_dia.strftime("%d"))
                    salida_logica = int(salida_jornada_globalf.strftime("%d"))
                    if sumador_dia2 == 30 or 31:
                        sumador_dia2 = 32
                    if salida_logica > sumador_dia2:
                        invalido = "La jornada de salida no puede ser de mas a dos días en fecha."
                        return render(request, 'crear_jornada.html', {'form': CrearjornadaForm, 'Invalido': invalido})
                    if salida_jornada_globalf <= inicio_jornada_globalf:
                        invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                        return render(request, 'crear_jornada.html', {'form': CrearjornadaForm, 'Invalido': invalido})
                    elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                        invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                        return render(request, 'crear_jornada.html', {'form': CrearjornadaForm, 'Invalido': invalido})
                    elif inicio_descanso_global2f is not None and salida_descanso_global2f is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_jornada_globalf or inicio_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 2 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f <= inicio_jornada_globalf or salida_descanso_global2f <= inicio_descanso_global2f:
                            invalido = "La jornada de salida de descanso 2 no puede ser menor al inicio de jornada o al incio de descanso 2."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 2 no puede ser mayor a la salida de jornada."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_descanso_globalf or inicio_descanso_global2f <= salida_descanso_globalf:
                            invalido = "La jornada de descanso 2 no puede coincidir con el descanso 1."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            print(request.POST)
                            nueva_jornada.save()
                            messages.success(
                                request, f"La jornada de {nueva_jornada.empleado.nombre} ha sido creada correctamente")
                            return redirect('crear_jornada')
                    else:
                        if salida_logica > sumador_dia2:
                            invalido = "La jornada de salida no puede ser de mas a dos días en fecha."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'crear_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f is not None and salida_descanso_global2f is not None:
                            if salida_jornada_globalf <= inicio_jornada_globalf:
                                invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                                invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                                invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                                invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_descanso_globalf >= salida_jornada_globalf:
                                invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif inicio_descanso_global2f <= inicio_jornada_globalf or inicio_descanso_global2f >= salida_jornada_globalf:
                                invalido = "La jornada de inicio de descanso 2 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_descanso_global2f <= inicio_jornada_globalf or salida_descanso_global2f <= inicio_descanso_global2f:
                                invalido = "La jornada de salida de descanso 2 no puede ser menor al inicio de jornada o al incio de descanso 2."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_descanso_global2f >= salida_jornada_globalf:
                                invalido = "La jornada de salida de descanso 2 no puede ser mayor a la salida de jornada."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif inicio_descanso_global2f <= inicio_descanso_globalf or inicio_descanso_global2f <= salida_descanso_globalf:
                                invalido = "La jornada de descanso 2 no puede coincidir con el descanso 1."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            else:
                                jornada_legalf = form.cleaned_data['jornada_legal']
                                horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf,
                                                    inicio_descanso_globalf,
                                                    salida_descanso_globalf,
                                                    inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                                nueva_jornada = form.save(commit=False)
                                nueva_jornada.total_horas = horarioo.total_horas
                                nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                                nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                                nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                                nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                                nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                                nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                                nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                                nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                                nueva_jornada.user = request.user
                                print(request.POST)
                                nueva_jornada.save()
                                messages.success(
                                    request,
                                    f"La jornada de {nueva_jornada.empleado.nombre} ha sido creada correctamente")
                                return redirect('crear_jornada')
                        elif inicio_descanso_globalf is not None and salida_descanso_globalf is not None:
                            if salida_jornada_globalf <= inicio_jornada_globalf:
                                invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                                invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                                invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                                invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            elif salida_descanso_globalf >= salida_jornada_globalf:
                                invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                                return render(request, 'crear_jornada.html',
                                              {'form': CrearjornadaForm, 'Invalido': invalido})
                            else:
                                jornada_legalf = form.cleaned_data['jornada_legal']
                                horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf,
                                                    inicio_descanso_globalf,
                                                    salida_descanso_globalf,
                                                    inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                                nueva_jornada = form.save(commit=False)
                                nueva_jornada.total_horas = horarioo.total_horas
                                nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                                nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                                nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                                nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                                nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                                nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                                nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                                nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                                nueva_jornada.user = request.user
                                print(request.POST)
                                nueva_jornada.save()
                                messages.success(
                                    request, f"La jornada de {nueva_jornada.empleado.nombre}")
                                return redirect('crear_jornada')
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            nueva_jornada.save()
                            messages.success(request,
                                             f"La jornada de {nueva_jornada.empleado.nombre} ha sido creada correctamente")
                            return redirect('crear_jornada')
                else:
                    return render(request, 'crear_jornada.html',
                                  {'form': CrearjornadaForm, 'error': 'Por Favor Escriba Datos Validos'})
            else:
                return HttpResponseForbidden("No tiene permisos para crear una jornada en talento humano")
        except ValueError:
            return render(request, 'crear_jornada.html',
                          {'form': CrearjornadaForm, 'error': 'Por Favor Escriba Datos Validos'})


@permission_required('nomina.view_jornada', raise_exception=True)
@login_required
def actualizar_jornada(request, jornada_id):
    if request.method == 'GET':
        jornada = get_object_or_404(Jornada, pk=jornada_id)
        form = CrearjornadaForm(instance=jornada)
        return render(request, 'actualizar_jornada.html', {'jornada': jornada, 'form': form})
    else:
        try:
            if request.user.has_perm('nomina.change_jornada'):
                empleado = get_object_or_404(Jornada, pk=jornada_id)
                form = CrearjornadaForm(request.POST, instance=empleado)
                if form.is_valid():
                    inicio_jornada_globalf = form.cleaned_data['inicio_jornada_global']
                    salida_jornada_globalf = form.cleaned_data['salida_jornada_global']
                    inicio_descanso_globalf = form.cleaned_data['inicio_descanso_global']
                    salida_descanso_globalf = form.cleaned_data['salida_descanso_global']
                    inicio_descanso_global2f = form.cleaned_data['inicio_descanso_global2']
                    salida_descanso_global2f = form.cleaned_data['salida_descanso_global2']
                    sumador_dia = inicio_jornada_globalf + timedelta(days=1)
                    sumador_dia2 = int(sumador_dia.strftime("%d"))
                    salida_logica = int(salida_jornada_globalf.strftime("%d"))
                    if sumador_dia2 == 30 or 31:
                        sumador_dia2 = 32
                    if salida_logica > sumador_dia2:
                        invalido = "La jornada de salida no puede ser de mas a dos días en fecha."
                        return render(request, 'actualizar_jornada.html',
                                      {'form': CrearjornadaForm, 'Invalido': invalido})
                    if salida_jornada_globalf <= inicio_jornada_globalf:
                        invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                        return render(request, 'actualizar_jornada.html',
                                      {'form': CrearjornadaForm, 'Invalido': invalido})
                    elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                        invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                        return render(request, 'actualizar_jornada.html',
                                      {'form': CrearjornadaForm, 'Invalido': invalido})
                    elif inicio_descanso_global2f is not None and salida_descanso_global2f is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, actualizar_jornada.html,
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_jornada_globalf or inicio_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 2 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f <= inicio_jornada_globalf or salida_descanso_global2f <= inicio_descanso_global2f:
                            invalido = "La jornada de salida de descanso 2 no puede ser menor al inicio de jornada o al incio de descanso 2."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 2 no puede ser mayor a la salida de jornada."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_descanso_globalf or inicio_descanso_global2f <= salida_descanso_globalf:
                            invalido = "La jornada de descanso 2 no puede coincidir con el descanso 1."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            nueva_jornada.save()
                            messages.success(request,
                                             f"La jornada de {nueva_jornada.empleado.nombre} ha sido actualizada correctamente")
                            return redirect('jornadas')
                    elif inicio_descanso_globalf is not None and salida_descanso_globalf is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'actualizar_jornada.html',
                                          {'form': CrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            nueva_jornada.save()
                            messages.success(request,
                                             f"La jornada de {nueva_jornada.empleado.nombre} ha sido actualizada correctamente")
                            return redirect('jornadas')
                    else:
                        jornada_legalf = form.cleaned_data['jornada_legal']
                        horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                            salida_descanso_globalf,
                                            inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                        nueva_jornada = form.save(commit=False)
                        nueva_jornada.total_horas = horarioo.total_horas
                        nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                        nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                        nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                        nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                        nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                        nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                        nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                        nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                        nueva_jornada.user = request.user
                        nueva_jornada.save()
                        messages.success(request,
                                         f"La jornada de {nueva_jornada.empleado.nombre} ha sido actualizada correctamente")
                        return redirect('jornadas')
                return redirect('jornadas')
            else:
                return HttpResponseForbidden("No tiene permisos para editar una jornada en talento humano")
        except ValueError:
            jornada = get_object_or_404(Jornada, pk=jornada_id)
            form = CrearjornadaForm(request.POST, instance=jornada)
            return render(request, 'actualizar_jornada.html',
                          {'jornada': jornada, 'form': form, 'error': "Error De Datos"})


@permission_required('nomina.view_jornada', raise_exception=True)
@login_required
def eliminar_jornada(request, jornada_id):
    if request.method == 'GET':
        jornada = get_object_or_404(Jornada, pk=jornada_id)
        form = CrearjornadaForm(instance=jornada)
        return render(request, 'eliminar_jornada.html', {'jornada': jornada, 'form': form})
    else:
        try:
            if request.user.has_perm('nomina.delete_jornada'):
                empleado = get_object_or_404(Jornada, pk=jornada_id)
                form = CrearjornadaForm(request.POST, instance=empleado)
                if form.is_valid():
                    inicio_jornada_globalf = form.cleaned_data['inicio_jornada_global']
                    salida_jornada_globalf = form.cleaned_data['salida_jornada_global']
                    inicio_descanso_globalf = form.cleaned_data['inicio_descanso_global']
                    salida_descanso_globalf = form.cleaned_data['salida_descanso_global']
                    inicio_descanso_global2f = form.cleaned_data['inicio_descanso_global2']
                    salida_descanso_global2f = form.cleaned_data['salida_descanso_global2']
                    jornada_legalf = form.cleaned_data['jornada_legal']
                    horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                        salida_descanso_globalf,
                                        inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                    nueva_jornada = form.save(commit=False)
                    nueva_jornada.total_horas = horarioo.total_horas
                    nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                    nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                    nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                    nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                    nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                    nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                    nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                    nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                    nueva_jornada.user = request.user
                    nueva_jornada.delete()
                    messages.error(request,
                                   f"La jornada de {nueva_jornada.empleado.nombre} ha sido eliminada correctamente")
                return redirect('jornadas')
            else:
                return HttpResponseForbidden("No tiene permisos para eliminar jornadas de talento humano")
        except ValueError:
            jornada = get_object_or_404(Jornada, pk=jornada_id)
            form = CrearjornadaForm(request.POST, instance=jornada)
            return render(request, 'eliminar_jornada.html', {'jornada': jornada, 'form': form,
                                                             'error': "Error De Datos"})


@permission_required('nomina.view_jornada', raise_exception=True)
@login_required
def list_jornadas(request):
    data = {}
    try:
        dia_actual = datetime.today()
        fechas_dos_meses = dia_actual - timedelta(days=30)
        todas_jornadas = Jornada.objects.filter(inicio_jornada_global__range=[
            fechas_dos_meses, dia_actual])
        registros = todas_jornadas.count()
        paginator = Paginator(todas_jornadas, registros)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['todas_jornadas'] = []
        for jornada in page_obj:
            jornada_dict = {
                'id': jornada.id,
                'empleado_nombre': jornada.empleado.nombre,
                'empleado_cedula': format(jornada.empleado.cedula, ',d').replace(',',
                                                                                 '.') if jornada.empleado.cedula else None,
                'inicio_jornada_global': jornada.inicio_jornada_global.strftime('%d/%m/%Y Hora:%H:%M'),
                'salida_jornada_global': jornada.salida_jornada_global.strftime('%d/%m/%Y  Hora:%H:%M'),
                'inicio_descanso_global': jornada.inicio_descanso_global.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.inicio_descanso_global else "-",
                'salida_descanso_global': jornada.salida_descanso_global.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.salida_descanso_global else "-",
                'inicio_descanso_global2': jornada.inicio_descanso_global2.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.inicio_descanso_global2 else "-",
                'salida_descanso_global2': jornada.salida_descanso_global2.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.salida_descanso_global2 else "-",
                'jornada_legal': jornada.jornada_legal,
                'total_horas': jornada.total_horas,
                'diurnas_totales': jornada.diurnas_totales,
                'nocturnas_totales': jornada.nocturnas_totales,
                'extras_diurnas_totales': jornada.extras_diurnas_totales,
                'extras_nocturnos_totales': jornada.extras_nocturnos_totales,
                'diurnos_festivo_totales': jornada.diurnos_festivo_totales,
                'nocturnos_festivo_totales': jornada.nocturnos_festivo_totales,
                'extras_diurnos_festivo_totales': jornada.extras_diurnos_festivo_totales,
                'extras_nocturnos_festivo_totales': jornada.extras_nocturnos_festivo_totales,
                'fh_transaccion': jornada.fh_transaccion.strftime('%d/%m/%Y  Hora:%H:%M'),
                'user_id': jornada.user.username,
            }
            data['todas_jornadas'].append(jornada_dict)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@permission_required('nomina.view_empleados', raise_exception=True)
@login_required
def empleados(request):
    return render(request, 'empleados.html')


@permission_required('nomina.view_empleados', raise_exception=True)
@login_required
def list_empleados(request):
    data = {}
    try:
        todas_empleados = Empleados.objects.all()
        registros = todas_empleados.count()
        paginator = Paginator(todas_empleados, registros)
        page = request.GET.get('page')
        empleados = paginator.get_page(page)
        data['todas_empleados'] = []
        for empleado in empleados:
            empleado_dict = {
                'id': empleado.id,
                'nombre': empleado.nombre,
                'tdoc': empleado.tdoc,
                'cedula': format(empleado.cedula, ',d').replace(',', '.') if empleado.cedula else None,
                'empresa': empleado.empresa,
                'estado': empleado.estado,
                'contrato': empleado.contrato,
                'area': empleado.area,
                'cargo': empleado.cargo.cargo,
                'salario': str("$") + format(empleado.salario, ',d').replace(',', '.') if empleado.salario else None,
                'generaextras': empleado.generaextras,
                'ingreso': empleado.ingreso.strftime('%d %B %Y') if empleado.ingreso else "-",
                'retiro': empleado.retiro.strftime('%d %B %Y') if empleado.retiro else "-",
            }
            data['todas_empleados'].append(empleado_dict)
            data['empleados_count'] = todas_empleados.count()
            data['pages_count'] = paginator.num_pages
            data['current_page'] = empleados.number
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@permission_required('nomina.view_empleados', raise_exception=True)
@login_required
def actualizar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleados, pk=empleado_id)

    if request.method == 'GET':
        form = CrearempleadoForm(instance=empleado)
        return render(request, 'actualizar_empleado.html', {'empleado': empleado, 'form': form})
    elif request.method == 'POST':
        if request.user.has_perm('nomina.change_empleados'):
            form = CrearempleadoForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f"El empleado {empleado.nombre} ha sido actualizado correctamente")
                return redirect('empleados')
            else:
                return render(request, 'actualizar_empleado.html',
                              {'empleado': empleado, 'form': form, 'error': "Error de datos"})
        else:
            return HttpResponseForbidden("No tiene permisos para editar un empleado.")


@permission_required('nomina.view_empleados', raise_exception=True)
@login_required
def crear_empleado(request):
    if request.method == 'GET':
        return render(request, 'crear_empleado.html', {'form': CrearempleadoForm})
    else:
        try:
            form = CrearempleadoForm(request.POST)
            if request.user.has_perm('nomina.add_empleados'):
                nuevo_empleado = form.save(commit=False)
                nuevo_empleado.save()
                messages.success(request, f"{nuevo_empleado.nombre}")
                return redirect('crear_empleado')
            else:
                return HttpResponseForbidden("No tienes permisos para crear un empleado.")
        except ValueError:
            return render(request, 'crear_empleado.html',
                          {'form': CrearempleadoForm, 'error': 'Por Favor Escriba Datos Validos'})


@permission_required('nomina.view_festivos', raise_exception=True)
@login_required
def crear_festivo(request):
    if request.method == 'GET':
        festivos_nombre = Festivos.objects.values_list('festivo', flat=True)
        return render(request, 'crear_festivo.html', {'form': CrearfestivoForm, 'festivos_nombre': festivos_nombre})
    else:
        try:
            if request.user.has_perm('nomina.add_festivos'):
                form = CrearfestivoForm(request.POST)
                nuevo_festivo = form.save(commit=False)
                nuevo_festivo.save()
                messages.success(
                    request, f"El día festivo {nuevo_festivo.festivo} se ha creado correctamente")
                return redirect('crear_festivo')
            else:
                return HttpResponseForbidden("No tienes permisos para crear un festivo")
        except ValueError:
            return render(request, 'crear_festivo.html',
                          {'form': CrearfestivoForm, 'error': 'Por Favor Escriba Datos Validos'})


@permission_required('nomina.view_cargos', raise_exception=True)
@login_required
def crear_cargo(request):
    if request.method == 'GET':
        cargos_nombre = Cargos.objects.values_list('cargo', flat=True)
        return render(request, 'crear_cargo.html', {'form': CrearcargoForm, 'cargos_nombre': cargos_nombre})
    else:
        try:
            if request.user.has_perm('nomina.add_cargos'):
                form = CrearcargoForm(request.POST)
                nuevo_cargo = form.save(commit=False)
                nuevo_cargo.save()
                messages.success(
                    request, f"El cargo {nuevo_cargo.cargo} ha sido creado correctamente")
                return redirect('crear_cargo')
            else:
                return HttpResponseForbidden("No tienes permisos para crear un cargo")
        except ValueError:
            return render(request, 'crear_cargo.html',
                          {'form': CrearcargoForm, 'error': 'Por Favor Escriba Datos Validos'})


@login_required
def salir(request):
    logout(request)
    return redirect('home')


# ----------------------------------- OPERACIONES ---------------------------------------------------------------------

def ope_home(request):
    return render(request, 'ope_home.html')


def ope_iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'ope_iniciar_sesion.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'ope_iniciar_sesion.html',
                          {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecto'})
        else:
            print(request.POST)
            login(request, user)
            return redirect('ope_home')


def ope_export_jor_excel(request):
    jornada_resource = OpeJornadasResource()
    dataset = jornada_resource.export()
    response = HttpResponse(dataset.xls,
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="jornadas_exportados_Operaciones.xls"'
    return response


def ope_importar_excel_jor(request):
    if request.method == 'POST':
        jornadas_resource = OpeJornadasResource()
        dataset = Dataset()
        new_jornada = request.FILES['jornadas']
        imported_data = dataset.load(new_jornada.read(), format='xlsx')
        for data in imported_data:
            horarioo = Horarios(data[1], data[2], data[3],
                                data[4], data[5], data[6], data[7])
            valor = OpeJornada(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                user=request.user,
                total_horas=horarioo.total_horas,
                diurnas_totales=horarioo.diurnas_totales,
                nocturnas_totales=horarioo.nocturnas_totales,
                extras_diurnas_totales=horarioo.extras_diurnas_totales,
                extras_nocturnos_totales=horarioo.extras_nocturnos_totales,
                diurnos_festivo_totales=horarioo.diurnos_festivo_totales,
                nocturnos_festivo_totales=horarioo.nocturnos_festivo_totales,
                extras_diurnos_festivo_totales=horarioo.extras_diurnos_festivo_totales,
                extras_nocturnos_festivo_totales=horarioo.extras_nocturnos_festivo_totales,
            )
            valor.save()
            messages.success(
                request, "Excel de jornadas operaciones importado correctamente")
    return render(request, 'ope_import_jornadas.html')


@permission_required('nomina.view_opejornada', raise_exception=True)
@login_required
def ope_jornadas(request):
    return render(request, 'ope_jornadas.html')


@permission_required('nomina.view_opejornada', raise_exception=True)
@login_required
def ope_crear_jornada(request):
    if request.method == 'GET':
        return render(request, 'ope_crear_jornada.html', {'form': OpeCrearjornadaForm})
    else:
        try:
            if request.user.has_perm('nomina.add_opejornada'):
                form = OpeCrearjornadaForm(request.POST)
                if form.is_valid():
                    inicio_jornada_globalf = form.cleaned_data['inicio_jornada_global']
                    salida_jornada_globalf = form.cleaned_data['salida_jornada_global']
                    inicio_descanso_globalf = form.cleaned_data['inicio_descanso_global']
                    salida_descanso_globalf = form.cleaned_data['salida_descanso_global']
                    inicio_descanso_global2f = form.cleaned_data['inicio_descanso_global2']
                    salida_descanso_global2f = form.cleaned_data['salida_descanso_global2']
                    sumador_dia = inicio_jornada_globalf + timedelta(days=1)
                    sumador_dia2 = int(sumador_dia.strftime("%d"))
                    salida_logica = int(salida_jornada_globalf.strftime("%d"))
                    if sumador_dia2 == 30 or 31:
                        sumador_dia2 = 32
                    if salida_logica > sumador_dia2:
                        invalido = "La jornada de salida no puede ser de mas a dos días en fecha."
                        return render(request, 'ope_crear_jornada.html',
                                      {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                    if salida_jornada_globalf <= inicio_jornada_globalf:
                        invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                        return render(request, 'ope_crear_jornada.html',
                                      {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                    elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                        invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                        return render(request, 'ope_crear_jornada.html',
                                      {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                    elif inicio_descanso_global2f is not None and salida_descanso_global2f is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_jornada_globalf or inicio_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 2 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f <= inicio_jornada_globalf or salida_descanso_global2f <= inicio_descanso_global2f:
                            invalido = "La jornada de salida de descanso 2 no puede ser menor al inicio de jornada o al incio de descanso 2."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 2 no puede ser mayor a la salida de jornada."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_descanso_globalf or inicio_descanso_global2f <= salida_descanso_globalf:
                            invalido = "La jornada de descanso 2 no puede coincidir con el descanso 1."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            nueva_jornada.save()
                            messages.success(
                                request, f"La jornada de {nueva_jornada.empleado.nombre} ha sido creada correctamente")
                            return redirect('ope_crear_jornada')
                    elif inicio_descanso_globalf is not None and salida_descanso_globalf is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'ope_crear_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            print(request.POST)
                            nueva_jornada.save()
                            messages.success(
                                request, f"La jornada de {nueva_jornada.empleado.nombre} ha sido creada correctamente")
                            return redirect('ope_crear_jornada')
                    else:
                        jornada_legalf = form.cleaned_data['jornada_legal']
                        horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                            salida_descanso_globalf,
                                            inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                        nueva_jornada = form.save(commit=False)
                        nueva_jornada.total_horas = horarioo.total_horas
                        nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                        nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                        nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                        nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                        nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                        nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                        nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                        nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                        nueva_jornada.user = request.user
                        nueva_jornada.save()
                        messages.success(
                            request, f"La jornada de {nueva_jornada.empleado.nombre} ha sido creada correctamente")
                        return redirect('ope_crear_jornada')
                else:
                    return render(request, 'ope_crear_jornada.html',
                                  {'form': OpeCrearjornadaForm, 'error': 'Por Favor Escriba Datos Validos'})
            else:
                return HttpResponseForbidden("No tiene permisos para crear jornadas en operaciones.")
        except ValueError:
            return render(request, 'ope_crear_jornada.html',
                          {'form': OpeCrearjornadaForm, 'error': 'Por Favor Escriba Datos Validos'})


@permission_required('nomina.view_opejornada', raise_exception=True)
@login_required
def ope_actualizar_jornada(request, jornada_id):
    if request.method == 'GET':
        jornada = get_object_or_404(OpeJornada, pk=jornada_id)
        form = OpeCrearjornadaForm(instance=jornada)
        return render(request, 'ope_actualizar_jornada.html', {'jornada': jornada, 'form': form})
    else:
        try:
            if request.user.has_perm('nomina.change_opejornada'):
                empleado = get_object_or_404(OpeJornada, pk=jornada_id)
                form = OpeCrearjornadaForm(request.POST, instance=empleado)
                if form.is_valid():
                    inicio_jornada_globalf = form.cleaned_data['inicio_jornada_global']
                    salida_jornada_globalf = form.cleaned_data['salida_jornada_global']
                    inicio_descanso_globalf = form.cleaned_data['inicio_descanso_global']
                    salida_descanso_globalf = form.cleaned_data['salida_descanso_global']
                    inicio_descanso_global2f = form.cleaned_data['inicio_descanso_global2']
                    salida_descanso_global2f = form.cleaned_data['salida_descanso_global2']
                    sumador_dia = inicio_jornada_globalf + timedelta(days=1)
                    sumador_dia2 = int(sumador_dia.strftime("%d"))
                    salida_logica = int(salida_jornada_globalf.strftime("%d"))
                    if sumador_dia2 == 30 or 31:
                        sumador_dia2 = 32
                    if salida_logica > sumador_dia2:
                        invalido = "La jornada de salida no puede ser de mas a dos días en fecha."
                        return render(request, 'ope_actualizar_jornada.html',
                                      {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                    if salida_jornada_globalf <= inicio_jornada_globalf:
                        invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                        return render(request, 'ope_actualizar_jornada.html',
                                      {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                    elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                        invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                        return render(request, 'ope_actualizar_jornada.html',
                                      {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                    elif inicio_descanso_global2f is not None and salida_descanso_global2f is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_jornada_globalf or inicio_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 2 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f <= inicio_jornada_globalf or salida_descanso_global2f <= inicio_descanso_global2f:
                            invalido = "La jornada de salida de descanso 2 no puede ser menor al inicio de jornada o al incio de descanso 2."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_global2f >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 2 no puede ser mayor a la salida de jornada."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_global2f <= inicio_descanso_globalf or inicio_descanso_global2f <= salida_descanso_globalf:
                            invalido = "La jornada de descanso 2 no puede coincidir con el descanso 1."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            nueva_jornada.save()
                            messages.success(
                                request,
                                f"La jornada de {nueva_jornada.empleado.nombre} ha sido actualizada correctamente")
                            return redirect('ope_jornadas')
                    elif inicio_descanso_globalf is not None and salida_descanso_globalf is not None:
                        if salida_jornada_globalf <= inicio_jornada_globalf:
                            invalido = "La jornada de salida no puede ser menor a la jornada de entrada."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_jornada_globalf >= (inicio_jornada_globalf + timedelta(hours=47)):
                            invalido = "La jornada de salida no puede ser de mas de un día respecto a la jornada de inicio."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif inicio_descanso_globalf <= inicio_jornada_globalf or inicio_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de inicio de descanso 1 no puede ser menor al inicio de jornada o mayor a la jornada de salida"
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf <= inicio_jornada_globalf or salida_descanso_globalf <= inicio_descanso_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser menor al inicio de jornada o al incio de descanso 1."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        elif salida_descanso_globalf >= salida_jornada_globalf:
                            invalido = "La jornada de salida de descanso 1 no puede ser mayor a la salida de jornada."
                            return render(request, 'ope_actualizar_jornada.html',
                                          {'form': OpeCrearjornadaForm, 'Invalido': invalido})
                        else:
                            jornada_legalf = form.cleaned_data['jornada_legal']
                            horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                                salida_descanso_globalf,
                                                inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                            nueva_jornada = form.save(commit=False)
                            nueva_jornada.total_horas = horarioo.total_horas
                            nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                            nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                            nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                            nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                            nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                            nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                            nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                            nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                            nueva_jornada.user = request.user
                            nueva_jornada.save()
                            messages.success(
                                request,
                                f"La jornada de {nueva_jornada.empleado.nombre} ha sido actualizada correctamente")
                            return redirect('ope_jornadas')
                    else:
                        jornada_legalf = form.cleaned_data['jornada_legal']
                        horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                            salida_descanso_globalf,
                                            inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                        nueva_jornada = form.save(commit=False)
                        nueva_jornada.total_horas = horarioo.total_horas
                        nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                        nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                        nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                        nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                        nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                        nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                        nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                        nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                        nueva_jornada.user = request.user
                        nueva_jornada.save()
                        messages.success(
                            request, f"La jornada de {nueva_jornada.empleado.nombre} ha sido actualizada correctamente")
                        return redirect('ope_jornadas')
                return redirect('ope_jornadas')
            else:
                return HttpResponseForbidden("No tiene permisos para editar jornadas de operaciones")
        except ValueError:
            jornada = get_object_or_404(OpeJornada, pk=jornada_id)
            form = OpeCrearjornadaForm(request.POST, instance=jornada)
            return render(request, 'ope_actualizar_jornada.html',
                          {'jornada': jornada, 'form': form, 'error': "Error De Datos"})


@permission_required('nomina.view_opejornada', raise_exception=True)
@login_required
def ope_eliminar_jornada(request, jornada_id):
    if request.method == 'GET':
        jornada = get_object_or_404(OpeJornada, pk=jornada_id)
        form = OpeCrearjornadaForm(instance=jornada)
        return render(request, 'ope_eliminar_jornada.html', {'jornada': jornada, 'form': form})
    else:
        try:
            if request.user.has_perm('nomina.delete_opejornada'):
                empleado = get_object_or_404(OpeJornada, pk=jornada_id)
                form = OpeCrearjornadaForm(request.POST, instance=empleado)
                if form.is_valid():
                    inicio_jornada_globalf = form.cleaned_data['inicio_jornada_global']
                    salida_jornada_globalf = form.cleaned_data['salida_jornada_global']
                    inicio_descanso_globalf = form.cleaned_data['inicio_descanso_global']
                    salida_descanso_globalf = form.cleaned_data['salida_descanso_global']
                    inicio_descanso_global2f = form.cleaned_data['inicio_descanso_global2']
                    salida_descanso_global2f = form.cleaned_data['salida_descanso_global2']
                    jornada_legalf = form.cleaned_data['jornada_legal']
                    horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf,
                                        salida_descanso_globalf,
                                        inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)
                    nueva_jornada = form.save(commit=False)
                    nueva_jornada.total_horas = horarioo.total_horas
                    nueva_jornada.diurnas_totales = horarioo.diurnas_totales
                    nueva_jornada.nocturnas_totales = horarioo.nocturnas_totales
                    nueva_jornada.extras_diurnas_totales = horarioo.extras_diurnas_totales
                    nueva_jornada.extras_nocturnos_totales = horarioo.extras_nocturnos_totales
                    nueva_jornada.diurnos_festivo_totales = horarioo.diurnos_festivo_totales
                    nueva_jornada.nocturnos_festivo_totales = horarioo.nocturnos_festivo_totales
                    nueva_jornada.extras_diurnos_festivo_totales = horarioo.extras_diurnos_festivo_totales
                    nueva_jornada.extras_nocturnos_festivo_totales = horarioo.extras_nocturnos_festivo_totales
                    nueva_jornada.user = request.user
                    nueva_jornada.delete()
                    messages.success(
                        request, f"La jornada de {nueva_jornada.empleado.nombre} ha sido eliminado correctamente")
                return redirect('ope_jornadas')
            else:
                return HttpResponseForbidden("No tiene permisos para eliminar una jornada en operaciones.")
        except ValueError:
            jornada = get_object_or_404(OpeJornada, pk=jornada_id)
            form = OpeCrearjornadaForm(request.POST, instance=jornada)
            return render(request, 'ope_eliminar_jornada.html', {'jornada': jornada, 'form': form,
                                                                 'error': "Error De Datos"})


@permission_required('nomina.view_opejornada', raise_exception=True)
@login_required
def ope_list_jornadas(request):
    data = {}
    try:
        dia_actual = datetime.today()
        fechas_dos_meses = dia_actual - timedelta(days=30)
        todas_jornadas = OpeJornada.objects.filter(inicio_jornada_global__range=[
            fechas_dos_meses, dia_actual])
        registros = todas_jornadas.count()
        paginator = Paginator(todas_jornadas, registros)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['todas_jornadas'] = []
        for jornada in page_obj:
            jornada_dict = {
                'id': jornada.id,
                'empleado_nombre': jornada.empleado.nombre,
                'empleado_cedula': format(jornada.empleado.cedula, ',d').replace(',',
                                                                                 '.') if jornada.empleado.cedula else None,
                'inicio_jornada_global': jornada.inicio_jornada_global.strftime('%d/%m/%Y Hora:%H:%M'),
                'salida_jornada_global': jornada.salida_jornada_global.strftime('%d/%m/%Y  Hora:%H:%M'),
                'inicio_descanso_global': jornada.inicio_descanso_global.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.inicio_descanso_global else "-",
                'salida_descanso_global': jornada.salida_descanso_global.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.salida_descanso_global else "-",
                'inicio_descanso_global2': jornada.inicio_descanso_global2.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.inicio_descanso_global2 else "-",
                'salida_descanso_global2': jornada.salida_descanso_global2.strftime(
                    '%d/%m/%Y  Hora:%H:%M') if jornada.salida_descanso_global2 else "-",
                'jornada_legal': jornada.jornada_legal,
                'total_horas': jornada.total_horas,
                'diurnas_totales': jornada.diurnas_totales,
                'nocturnas_totales': jornada.nocturnas_totales,
                'extras_diurnas_totales': jornada.extras_diurnas_totales,
                'extras_nocturnos_totales': jornada.extras_nocturnos_totales,
                'diurnos_festivo_totales': jornada.diurnos_festivo_totales,
                'nocturnos_festivo_totales': jornada.nocturnos_festivo_totales,
                'extras_diurnos_festivo_totales': jornada.extras_diurnos_festivo_totales,
                'extras_nocturnos_festivo_totales': jornada.extras_nocturnos_festivo_totales,
                'fh_transaccion': jornada.fh_transaccion.strftime('%d/%m/%Y  Hora:%H:%M'),
                'user_id': jornada.user.username,
            }
            data['todas_jornadas'].append(jornada_dict)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@permission_required('nomina.view_empleados', raise_exception=True)
@login_required
def ope_empleados(request):
    return render(request, 'ope_empleados.html')


@permission_required('nomina.view_empleados', raise_exception=True)
@login_required
def ope_list_empleados(request):
    data = {}
    try:
        todas_empleados = Empleados.objects.all()
        registros = todas_empleados.count()
        paginator = Paginator(todas_empleados, registros)
        page = request.GET.get('page')
        empleados = paginator.get_page(page)
        data['todas_empleados'] = []
        for empleado in empleados:
            empleado_dict = {
                'id': empleado.id,
                'nombre': empleado.nombre,
                'tdoc': empleado.tdoc,
                'cedula': format(empleado.cedula, ',d').replace(',', '.') if empleado.cedula else None,
                'empresa': empleado.empresa,
                'estado': empleado.estado,
                'contrato': empleado.contrato,
                'area': empleado.area,
                'cargo': empleado.cargo.cargo,
                'salario': str("$") + format(empleado.salario, ',d').replace(',', '.') if empleado.salario else None,
                'generaextras': empleado.generaextras,
                'ingreso': empleado.ingreso.strftime('%d %B %Y') if empleado.ingreso else "-",
                'retiro': empleado.retiro.strftime('%d %B %Y') if empleado.retiro else "-",
            }
            data['todas_empleados'].append(empleado_dict)
            data['empleados_count'] = todas_empleados.count()
            data['pages_count'] = paginator.num_pages
            data['current_page'] = empleados.number
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@permission_required('nomina.view_festivos', raise_exception=True)
@login_required
def ope_crear_festivo(request):
    festivos_nombre = Festivos.objects.values_list('festivo', flat=True)
    return render(request, 'ope_crear_festivo.html', {'festivos_nombre': festivos_nombre})


@permission_required('nomina.view_festivos', raise_exception=True)
@login_required
def ope_crear_cargo(request):
    cargos_nombre = Cargos.objects.values_list('cargo', flat=True)
    return render(request, 'ope_crear_cargo.html', {'cargos_nombre': cargos_nombre})
