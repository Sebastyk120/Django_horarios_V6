from django.db import models
from django.contrib.auth.models import User
from .choices import estados, empresas, area, extras
from django.forms import TextInput
from django.utils import formats

# Widgets Personalizados


class SeparadorDeMiles(TextInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', 'type': 'text'})

    def format_value(self, value):
        if value is None:
            return ''
        return formats.number_format(value, use_l10n=True)

# Modelos APP Heavens.


class Cargos(models.Model):
    cargo = models.CharField(max_length=60, verbose_name="Cargo")

    class Meta:
        ordering = ['cargo']

    def __str__(self):
        return str(self.cargo)


class Empleados(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Empleado")
    cedula = models.IntegerField(verbose_name="Cedula Empleado")
    empresa = models.CharField(max_length=100, choices=empresas,
                               default='Heavens Fruits SAS', verbose_name="Empresa")
    estado = models.CharField(
        max_length=10, choices=estados, default='Activo', verbose_name="Estado")
    area = models.CharField(max_length=33, choices=area, verbose_name="Area")
    cargo = models.ForeignKey(
        Cargos, on_delete=models.CASCADE, verbose_name="Cargo")
    salario = models.IntegerField(verbose_name="Salario")
    generaextras = models.CharField(
        max_length=2, choices=extras, default='No', verbose_name="Genera Extras")
    ingreso = models.DateField(
        max_length=10, verbose_name="Fecha Ingreso", null=True)
    retiro = models.DateField(
        max_length=10, verbose_name="Fecha Retiro", null=True, blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre + '  -Cedula: ' + str(self.cedula) + ' -Estado: ' + self.estado


class Jornada(models.Model):
    inicio_jornada_global = models.DateTimeField(
        null=True, verbose_name="Inicio Jornada")
    salida_jornada_global = models.DateTimeField(
        null=True, verbose_name="Salida Jornada")
    inicio_descanso_global = models.DateTimeField(
        blank=True, null=True, verbose_name="Inicio Descanso")
    salida_descanso_global = models.DateTimeField(
        blank=True, null=True, verbose_name="Salida Descanso")
    inicio_descanso_global2 = models.DateTimeField(
        blank=True, null=True, verbose_name="Inicio Descanso 2")
    salida_descanso_global2 = models.DateTimeField(
        blank=True, null=True, verbose_name="Salida Descanso 2")
    jornada_legal = models.IntegerField(
        default=8, verbose_name="Jornada Legal")
    total_horas = models.FloatField(verbose_name="Total Horas", default=0)
    diurnas_totales = models.FloatField(
        verbose_name="Horas Diurnas", default=0)
    nocturnas_totales = models.FloatField(
        verbose_name="Horas Nocturnas", default=0)
    extras_diurnas_totales = models.FloatField(
        verbose_name="Horas Extras Diurnas", default=0)
    extras_nocturnos_totales = models.FloatField(
        verbose_name=" Horas Extras Nocturnas", default=0)
    diurnos_festivo_totales = models.FloatField(
        verbose_name="Horas Diurnas Festivas", default=0)
    nocturnos_festivo_totales = models.FloatField(
        verbose_name="Horas Nocturnas Festivas", default=0)
    extras_diurnos_festivo_totales = models.FloatField(
        verbose_name="Horas Extras Diurnas Festivas", default=0)
    extras_nocturnos_festivo_totales = models.FloatField(
        verbose_name="Horas Extras Nocturnas Festivas", default=0)
    fh_transaccion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha De Transacción")
    empleado = models.ForeignKey(
        Empleados, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, verbose_name="Creada Por")

    class Meta:
        ordering = ['empleado']

    def __str__(self):
        return str(self.empleado.nombre) + ' -Fecha Liquidada: ' + str(self.inicio_descanso_global)
