from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Jornada, Empleados
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import CrearjornadaForm, CrearempleadoForm
from .calc_horarios import Horarios
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def home(request):
    return render(request, 'home.html')


@user_passes_test(lambda u: u.is_superuser)
def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario.
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('jornadas')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, "error": 'El usuario ya existe'})
        return render(request, 'signup.html', {'form': UserCreationForm, "error": 'Las contraseñas no coinciden'})


@login_required
def jornadas(request):
    return render(request, 'jornadas.html')


@login_required
def list_jornadas(request):
    data = {}
    try:
        todas_jornadas = Jornada.objects.all()
        data['todas_jornadas'] = []
        for jornada in todas_jornadas:
            jornada_dict = {
                'id': jornada.id,
                'inicio_jornada_global': jornada.inicio_jornada_global,
                'salida_jornada_global': jornada.salida_jornada_global,
                'inicio_descanso_global': jornada.inicio_descanso_global,
                'salida_descanso_global': jornada.salida_descanso_global,
                'inicio_descanso_global2': jornada.inicio_descanso_global2,
                'salida_descanso_global2': jornada.salida_descanso_global2,
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
                'fh_transaccion': jornada.fh_transaccion,
                'empleado_nombre': jornada.empleado.nombre,
                'user_id': jornada.user.username,
            }
            data['todas_jornadas'].append(jornada_dict)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@login_required()
def empleados(request):
    return render(request, 'empleados.html')


@login_required
def list_empleados(request):
    todas_empleados = list(Empleados.objects.values())
    data = {'todas_empleados': todas_empleados}
    return JsonResponse(data)


@login_required
def actualizar_empleado(request, empleado_id):
    if request.method == 'GET':
        empleado = get_object_or_404(Empleados, pk=empleado_id)
        form = CrearempleadoForm(instance=empleado)
        return render(request, 'actualizar_empleado.html', {'empleado': empleado, 'form': form})
    else:
        try:
            empleado = get_object_or_404(Empleados, pk=empleado_id)
            form = CrearempleadoForm(request.POST, instance=empleado)
            form.save()
            return redirect('empleados')
        except ValueError:
            empleado = get_object_or_404(Empleados, pk=empleado_id)
            form = CrearempleadoForm(request.POST, instance=empleado)
            return render(request, 'actualizar_empleado.html', {'empleado': empleado, 'form': form,
                                                                'error': "Error De Datos"})


@login_required
def crear_jornada(request):
    if request.method == 'GET':
        return render(request, 'crear_jornada.html', {'form': CrearjornadaForm})
    else:
        try:
            form = CrearjornadaForm(request.POST)
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
                nueva_jornada.save()
                return redirect('jornadas')
            else:
                return render(request, 'crear_jornada.html',
                              {'form': CrearjornadaForm, 'error': 'Por Favor Escriba Datos Validos'})
        except ValueError:
            return render(request, 'crear_jornada.html',
                          {'form': CrearjornadaForm, 'error': 'Por Favor Escriba Datos Validos'})


@login_required
def actualizar_jornada(request, jornada_id):
    if request.method == 'GET':
        jornada = get_object_or_404(Jornada, pk=jornada_id)
        form = CrearjornadaForm(instance=jornada)
        return render(request, 'actualizar_jornada.html', {'jornada': jornada, 'form': form})
    else:
        try:
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
                nueva_jornada.save()
            return redirect('jornadas')
        except ValueError:
            jornada = get_object_or_404(Jornada, pk=jornada_id)
            form = CrearjornadaForm(request.POST, instance=jornada)
            return render(request, 'actualizar_jornada.html', {'jornada': jornada, 'form': form,
                                                               'error': "Error De Datos"})


@login_required
def crear_empleado(request):
    if request.method == 'GET':
        return render(request, 'crear_empleado.html', {'form': CrearempleadoForm})
    else:
        try:
            form = CrearempleadoForm(request.POST)
            nuevo_empleado = form.save(commit=False)
            nuevo_empleado.save()
            return redirect('home')
        except ValueError:
            return render(request, 'crear_empleado.html',
                          {'form': CrearempleadoForm, 'error': 'Por Favor Escriba Datos Validos'})


@login_required
def salir(request):
    logout(request)
    return redirect('home')


def loguearte(request):
    if request.method == 'GET':
        return render(request, 'loguearte.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'loguearte.html',
                          {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecto'})
        else:
            print(request.POST)
            login(request, user)
            return redirect('home')
