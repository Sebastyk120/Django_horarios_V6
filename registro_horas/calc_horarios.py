import locale
from datetime import datetime, timedelta
from .models import Festivos

locale.setlocale(locale.LC_ALL, ("esp", "UTF-8"))


class Horarios:
    def __init__(self, inicio_jornada_global, salida_jornada_global, inicio_descanso_global, salida_descanso_global,
                 inicio_descanso_global2, salida_descanso_global2, jornada_legal):
        self.inicio_jornada_global = inicio_jornada_global
        self.salida_jornada_global = salida_jornada_global
        self.inicio_descanso_global = inicio_descanso_global
        self.salida_descanso_global = salida_descanso_global
        self.inicio_descanso_global2 = inicio_descanso_global2
        self.salida_descanso_global2 = salida_descanso_global2
        self.jornada_legal = jornada_legal
        self.total_horas = 0
        self.diurnas_totales = 0
        self.nocturnas_totales = 0
        self.extras_diurnas_totales = 0
        self.extras_nocturnos_totales = 0
        self.diurnos_festivo_totales = 0
        self.nocturnos_festivo_totales = 0
        self.extras_diurnos_festivo_totales = 0
        self.extras_nocturnos_festivo_totales = 0

        def enteros():
            inicio_dia_semana = datetime.strftime(
                self.inicio_jornada_global, "%A")
            inicio_year = int(datetime.strftime(
                self.inicio_jornada_global, "%Y"))
            inicio_mes = int(datetime.strftime(
                self.inicio_jornada_global, "%m"))
            inicio_dia = int(datetime.strftime(
                self.inicio_jornada_global, "%d"))
            salida_dia_semana = datetime.strftime(
                self.salida_jornada_global, "%A")
            salida_year = int(datetime.strftime(
                self.salida_jornada_global, "%Y"))
            salida_mes = int(datetime.strftime(
                self.salida_jornada_global, "%m"))
            salida_dia = int(datetime.strftime(
                self.salida_jornada_global, "%d"))
            jornada_legal_minutos = self.jornada_legal * 60

            def calculohoras():
                # ------------------------------------Lista De Festivos Colombia 2023 -------------------------------
                def festivos():
                    festivos_lista = []
                    objetos_festivo = Festivos.objects.all()
                    for festivo in objetos_festivo:
                        festivos_lista.append(festivo.festivo.strftime('%Y-%m-%d'))
                    inicio_jornada_global_festivo = datetime.strftime(
                        self.inicio_jornada_global, "%Y-%m-%d")
                    salida_jornada_global_festivo = datetime.strftime(
                        self.salida_jornada_global, "%Y-%m-%d")
                    if inicio_jornada_global_festivo in festivos_lista:
                        inicio_dia_festivo = "festivo"
                    else:
                        inicio_dia_festivo = ""
                    if salida_jornada_global_festivo in festivos_lista:
                        salida_dia_festivo = "festivo"
                    else:
                        salida_dia_festivo = ""
                    return inicio_dia_festivo, salida_dia_festivo

                festivo_inicio, festivo_salida = festivos()

                def jornada_un_descanso():
                    # --------------- Jornada con Dia diferente ------------------------------------------
                    if inicio_dia != salida_dia:
                        # ------------------------------------- Día 1 ------------------------------------------------
                        minutos_diurnos_dia1 = 0
                        minutos_nocturnos_dia1 = 0
                        minutos_totales_dia1 = 0
                        minutos_extras_diurnos_dia1 = 0
                        minutos_extras_nocturnos_dia1 = 0
                        minutos_diurnos_festivo_dia1 = 0
                        minutos_nocturnos_festivo_dia1 = 0
                        minutos_extras_diurnos_festivo_dia1 = 0
                        minutos_extras_nocturnos_festivo_dia1 = 0
                        diurno1 = datetime(
                            inicio_year, inicio_mes, inicio_dia, 6, 0)
                        nocturno1 = datetime(
                            inicio_year, inicio_mes, inicio_dia, 21, 00)
                        salida_jornada = datetime(
                            salida_year, salida_mes, salida_dia, 0, 0)
                        while self.inicio_jornada_global <= salida_jornada:
                            self.inicio_jornada_global += timedelta(minutes=1)
                            minutos_totales_dia1 = minutos_totales_dia1 + 1
                            # ------------------------------Acumulador de Descansos --------------------------------
                            if self.inicio_descanso_global <= self.inicio_jornada_global <= self.salida_descanso_global:
                                self.inicio_jornada_global += timedelta(
                                    minutes=1)
                                minutos_totales_dia1 = minutos_totales_dia1 - 1
                            elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                                if minutos_totales_dia1 > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_extras_nocturnos_festivo_dia1 = \
                                            minutos_extras_nocturnos_festivo_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                                    else:
                                        minutos_extras_diurnos_festivo_dia1 = minutos_extras_diurnos_festivo_dia1 + 1
                                else:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                                    else:
                                        minutos_diurnos_festivo_dia1 = minutos_diurnos_festivo_dia1 + 1
                            # ---------------------------- Acumulador de Extras día 1 --------------------------------
                            else:
                                if minutos_totales_dia1 > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                                    else:
                                        minutos_extras_diurnos_dia1 = minutos_extras_diurnos_dia1 + 1
                                else:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                                    else:
                                        minutos_diurnos_dia1 = minutos_diurnos_dia1 + 1

                        # # ---------------------------- Acumulador de Extras día 2 o más -----------------------------
                        consolidado_minutos = minutos_totales_dia1
                        minutos_diurnos_dia2 = 0
                        minutos_nocturnos_dia2 = 0
                        minutos_totales_dia2 = 0
                        minutos_extras_diurnos_dia2 = 0
                        minutos_extras_nocturnos_dia2 = 0
                        minutos_diurnos_festivo_dia2 = 0
                        minutos_nocturnos_festivo_dia2 = 0
                        minutos_extras_diurnos_festivo_dia2 = 0
                        minutos_extras_nocturnos_festivo_dia2 = 0
                        diurno2 = datetime(
                            salida_year, salida_mes, salida_dia, 6, 0)
                        nocturno2 = datetime(
                            salida_year, salida_mes, salida_dia, 21, 00)
                        inicio_jornada2 = datetime(
                            salida_year, salida_mes, salida_dia, 0, 0)
                        salida_jornada2 = self.salida_jornada_global
                        inicio_dia_semana2 = inicio_jornada2.strftime("%A")
                        while inicio_jornada2 <= salida_jornada2:
                            inicio_jornada2 += timedelta(minutes=1)
                            minutos_totales_dia2 = minutos_totales_dia2 + 1
                            consolidado2 = consolidado_minutos + minutos_totales_dia2
                            # ------------------------------Acumulador de Descansos --------------------------------
                            if self.inicio_descanso_global <= inicio_jornada2 <= self.salida_descanso_global:
                                inicio_jornada2 += timedelta(minutes=1)
                                minutos_totales_dia2 = minutos_totales_dia2 - 1

                            elif inicio_dia_semana2 == "domingo" or festivo_salida == "festivo":
                                if consolidado2 > jornada_legal_minutos:
                                    if inicio_jornada2 < diurno2:
                                        minutos_extras_nocturnos_festivo_dia2 = \
                                            minutos_extras_nocturnos_festivo_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_extras_nocturnos_festivo_dia2 = minutos_extras_nocturnos_festivo_dia2 + 1
                                    else:
                                        minutos_extras_diurnos_festivo_dia2 = minutos_extras_diurnos_festivo_dia2 + 1
                                else:
                                    if inicio_jornada2 < diurno2:
                                        minutos_nocturnos_festivo_dia2 = minutos_nocturnos_festivo_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_nocturnos_festivo_dia2 = minutos_nocturnos_festivo_dia2 + 1
                                    else:
                                        minutos_diurnos_festivo_dia2 = minutos_diurnos_festivo_dia2 + 1
                            else:
                                if consolidado2 > jornada_legal_minutos:
                                    if inicio_jornada2 < diurno2:
                                        minutos_extras_nocturnos_dia2 = minutos_extras_nocturnos_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_extras_nocturnos_dia2 = minutos_extras_nocturnos_dia2 + 1
                                    else:
                                        minutos_extras_diurnos_dia2 = minutos_extras_diurnos_dia2 + 1
                                else:
                                    if inicio_jornada2 < diurno2:
                                        minutos_nocturnos_dia2 = minutos_nocturnos_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_nocturnos_dia2 = minutos_nocturnos_dia2 + 1
                                    else:
                                        minutos_diurnos_dia2 = minutos_diurnos_dia2 + 1
                        self.total_horas = round(
                            (minutos_totales_dia2 + consolidado_minutos) / 60, 1)
                        self.diurnas_totales = round(
                            (minutos_diurnos_dia1 + minutos_diurnos_dia2) / 60, 1)
                        self.nocturnas_totales = round(
                            (minutos_nocturnos_dia1 + minutos_nocturnos_dia2) / 60, 1)
                        self.extras_diurnas_totales = round(
                            (minutos_extras_diurnos_dia1 +
                             minutos_extras_diurnos_dia2) / 60,
                            1)
                        self.extras_nocturnos_totales = round(
                            (minutos_extras_nocturnos_dia1 + minutos_extras_nocturnos_dia2) / 60, 1)
                        self.diurnos_festivo_totales = round(
                            (minutos_diurnos_festivo_dia1 +
                             minutos_diurnos_festivo_dia2) / 60,
                            1)
                        self.nocturnos_festivo_totales = round(
                            (minutos_nocturnos_festivo_dia1 + minutos_nocturnos_festivo_dia2) / 60, 1)
                        self.extras_diurnos_festivo_totales = round(
                            (minutos_extras_diurnos_festivo_dia1 + minutos_extras_diurnos_festivo_dia2) / 60, 1)
                        self.extras_nocturnos_festivo_totales = round(
                            (minutos_extras_nocturnos_festivo_dia1 + minutos_extras_nocturnos_festivo_dia2) / 60, 1)
                    # ------------------------------------- Jornada mismo día---- 1 Descanso ---------------
                    else:
                        diurno = datetime(
                            inicio_year, inicio_mes, inicio_dia, 6, 0)
                        nocturno = datetime(
                            inicio_year, inicio_mes, inicio_dia, 21, 00)
                        minutos_totales = 0
                        minutos_diurnos = 0
                        minutos_nocturnos = 0
                        minutos_extras_diurnos = 0
                        minutos_extras_nocturnos = 0
                        minutos_diurnos_festivo = 0
                        minutos_nocturnos_festivo = 0
                        minutos_extras_diurnos_festivo = 0
                        minutos_extras_nocturnos_festivo = 0
                        while self.inicio_jornada_global <= self.salida_jornada_global:
                            self.inicio_jornada_global += timedelta(minutes=1)
                            minutos_totales = minutos_totales + 1
                            # ------------------------------Acumulador de Descansos --------------------------------
                            if self.inicio_descanso_global <= self.inicio_jornada_global <= self.salida_descanso_global:
                                self.inicio_jornada_global += timedelta(
                                    minutes=1)
                                minutos_totales = minutos_totales - 1

                                # ---------------------------- Acumulador de Festivos----------
                                # --------------------------------
                            elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                                # ---------------------------- Acumulador de Extras Festivos
                                # --------------------------------
                                if minutos_totales > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                                    else:
                                        minutos_extras_diurnos_festivo = minutos_extras_diurnos_festivo + 1
                                else:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                                    else:
                                        minutos_diurnos_festivo = minutos_diurnos_festivo + 1

                            # ---------------------------- Acumulador de Diurnos Normales -----------------------------
                            else:
                                # ---------------------------- Acumulador de  Extras Normales
                                # --------------------------------
                                if minutos_totales > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                                    else:
                                        minutos_extras_diurnos = minutos_extras_diurnos + 1
                                else:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_nocturnos = minutos_nocturnos + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_nocturnos = minutos_nocturnos + 1
                                    else:
                                        minutos_diurnos = minutos_diurnos + 1

                        self.total_horas = round(minutos_totales / 60, 1)
                        self.diurnas_totales = round(minutos_diurnos / 60, 1)
                        self.nocturnas_totales = round(
                            minutos_nocturnos / 60, 1)
                        self.extras_diurnas_totales = round(
                            minutos_extras_diurnos / 60, 1)
                        self.extras_nocturnos_totales = round(
                            minutos_extras_nocturnos / 60, 1)
                        self.diurnos_festivo_totales = round(
                            minutos_diurnos_festivo / 60, 1)
                        self.nocturnos_festivo_totales = round(
                            minutos_nocturnos_festivo / 60, 1)
                        self.extras_diurnos_festivo_totales = round(
                            minutos_extras_diurnos_festivo / 60, 1)
                        self.extras_nocturnos_festivo_totales = round(
                            minutos_extras_nocturnos_festivo / 60, 1)

                def jornada_dos_descansos():
                    # --------------- Jornada con Dia diferente ------------------------------------------
                    if inicio_dia != salida_dia:
                        # ------------------------------------- Día 1 -------------------------------------------------
                        minutos_diurnos_dia1 = 0
                        minutos_nocturnos_dia1 = 0
                        minutos_totales_dia1 = 0
                        minutos_extras_diurnos_dia1 = 0
                        minutos_extras_nocturnos_dia1 = 0
                        minutos_diurnos_festivo_dia1 = 0
                        minutos_nocturnos_festivo_dia1 = 0
                        minutos_extras_diurnos_festivo_dia1 = 0
                        minutos_extras_nocturnos_festivo_dia1 = 0
                        diurno1 = datetime(
                            inicio_year, inicio_mes, inicio_dia, 6, 0)
                        nocturno1 = datetime(
                            inicio_year, inicio_mes, inicio_dia, 21, 00)
                        salida_jornada = datetime(
                            salida_year, salida_mes, salida_dia, 0, 0)
                        while self.inicio_jornada_global <= salida_jornada:
                            self.inicio_jornada_global += timedelta(minutes=1)
                            minutos_totales_dia1 = minutos_totales_dia1 + 1
                            # ------------------------------Acumulador de Descansos --------------------------------
                            if self.inicio_descanso_global <= self.inicio_jornada_global <= \
                                    self.salida_descanso_global or self.inicio_descanso_global2 <= \
                                    self.inicio_jornada_global <= self.salida_descanso_global2:
                                self.inicio_jornada_global += timedelta(minutes=1)
                                minutos_totales_dia1 = minutos_totales_dia1 - 1

                            elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                                if minutos_totales_dia1 > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                                    else:
                                        minutos_extras_diurnos_festivo_dia1 = minutos_extras_diurnos_festivo_dia1 + 1
                                else:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                                    else:
                                        minutos_diurnos_festivo_dia1 = minutos_diurnos_festivo_dia1 + 1
                            # ---------------------------- Acumulador de Extras día 1 --------------------------------
                            else:
                                if minutos_totales_dia1 > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                                    else:
                                        minutos_extras_diurnos_dia1 = minutos_extras_diurnos_dia1 + 1
                                else:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                                    else:
                                        minutos_diurnos_dia1 = minutos_diurnos_dia1 + 1

                        # # ---------------------------- Acumulador de Extras día 2 o más -----------------------------
                        consolidado_minutos = minutos_totales_dia1
                        minutos_diurnos_dia2 = 0
                        minutos_nocturnos_dia2 = 0
                        minutos_totales_dia2 = 0
                        minutos_extras_diurnos_dia2 = 0
                        minutos_extras_nocturnos_dia2 = 0
                        minutos_diurnos_festivo_dia2 = 0
                        minutos_nocturnos_festivo_dia2 = 0
                        minutos_extras_diurnos_festivo_dia2 = 0
                        minutos_extras_nocturnos_festivo_dia2 = 0
                        diurno2 = datetime(
                            salida_year, salida_mes, salida_dia, 6, 0)
                        nocturno2 = datetime(
                            salida_year, salida_mes, salida_dia, 21, 00)
                        inicio_jornada2 = datetime(
                            salida_year, salida_mes, salida_dia, 0, 0)
                        salida_jornada2 = self.salida_jornada_global
                        inicio_dia_semana2 = inicio_jornada2.strftime("%A")
                        while inicio_jornada2 <= salida_jornada2:
                            inicio_jornada2 += timedelta(minutes=1)
                            minutos_totales_dia2 = minutos_totales_dia2 + 1
                            consolidado2 = consolidado_minutos + minutos_totales_dia2
                            # ------------------------------Acumulador de Descansos --------------------------------
                            if self.inicio_descanso_global <= inicio_jornada2 <= self.salida_descanso_global or \
                                    self.inicio_descanso_global2 <= inicio_jornada2 <= self.salida_descanso_global2:
                                inicio_jornada2 += timedelta(minutes=1)
                                minutos_totales_dia2 = minutos_totales_dia2 - 1

                            elif inicio_dia_semana2 == "domingo" or festivo_salida == "festivo":
                                if consolidado2 > jornada_legal_minutos:
                                    if inicio_jornada2 < diurno2:
                                        minutos_extras_nocturnos_festivo_dia2 = minutos_extras_nocturnos_festivo_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_extras_nocturnos_festivo_dia2 = minutos_extras_nocturnos_festivo_dia2 + 1
                                    else:
                                        minutos_extras_diurnos_festivo_dia2 = minutos_extras_diurnos_festivo_dia2 + 1
                                else:
                                    if inicio_jornada2 < diurno2:
                                        minutos_nocturnos_festivo_dia2 = minutos_nocturnos_festivo_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_nocturnos_festivo_dia2 = minutos_nocturnos_festivo_dia2 + 1
                                    else:
                                        minutos_diurnos_festivo_dia2 = minutos_diurnos_festivo_dia2 + 1
                            else:
                                if consolidado2 > jornada_legal_minutos:
                                    if inicio_jornada2 < diurno2:
                                        minutos_extras_nocturnos_dia2 = minutos_extras_nocturnos_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_extras_nocturnos_dia2 = minutos_extras_nocturnos_dia2 + 1
                                    else:
                                        minutos_extras_diurnos_dia2 = minutos_extras_diurnos_dia2 + 1
                                else:
                                    if inicio_jornada2 < diurno2:
                                        minutos_nocturnos_dia2 = minutos_nocturnos_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_nocturnos_dia2 = minutos_nocturnos_dia2 + 1
                                    else:
                                        minutos_diurnos_dia2 = minutos_diurnos_dia2 + 1
                        self.total_horas = round(
                            (minutos_totales_dia2 + consolidado_minutos) / 60, 1)
                        self.diurnas_totales = round(
                            (minutos_diurnos_dia1 + minutos_diurnos_dia2) / 60, 1)
                        self.nocturnas_totales = round(
                            (minutos_nocturnos_dia1 + minutos_nocturnos_dia2) / 60, 1)
                        self.extras_diurnas_totales = round(
                            (minutos_extras_diurnos_dia1 +
                             minutos_extras_diurnos_dia2) / 60,
                            1)
                        self.extras_nocturnos_totales = round(
                            (minutos_extras_nocturnos_dia1 + minutos_extras_nocturnos_dia2) / 60, 1)
                        self.diurnos_festivo_totales = round(
                            (minutos_diurnos_festivo_dia1 +
                             minutos_diurnos_festivo_dia2) / 60,
                            1)
                        self.nocturnos_festivo_totales = round(
                            (minutos_nocturnos_festivo_dia1 + minutos_nocturnos_festivo_dia2) / 60, 1)
                        self.extras_diurnos_festivo_totales = round(
                            (minutos_extras_diurnos_festivo_dia1 + minutos_extras_diurnos_festivo_dia2) / 60, 1)
                        self.extras_nocturnos_festivo_totales = round(
                            (minutos_extras_nocturnos_festivo_dia1 + minutos_extras_nocturnos_festivo_dia2) / 60, 1)
                        # ------------------------------------- Jornada mismo día ---- 2 Descansos ---------------
                    else:
                        diurno = datetime(
                            inicio_year, inicio_mes, inicio_dia, 6, 0)
                        nocturno = datetime(
                            inicio_year, inicio_mes, inicio_dia, 21, 00)
                        minutos_totales = 1
                        minutos_diurnos = 0
                        minutos_nocturnos = 0
                        minutos_extras_diurnos = 0
                        minutos_extras_nocturnos = 0
                        minutos_diurnos_festivo = 0
                        minutos_nocturnos_festivo = 0
                        minutos_extras_diurnos_festivo = 0
                        minutos_extras_nocturnos_festivo = 0
                        while self.inicio_jornada_global <= self.salida_jornada_global:
                            self.inicio_jornada_global += timedelta(minutes=1)
                            minutos_totales = minutos_totales + 1
                            # ------------------------------Acumulador de Descansos --------------------------------
                            if self.inicio_descanso_global <= self.inicio_jornada_global <= \
                                    self.salida_descanso_global or self.inicio_descanso_global2 <= \
                                    self.inicio_jornada_global <= self.salida_descanso_global2:
                                self.inicio_jornada_global += timedelta(
                                    minutes=1)
                                minutos_totales = minutos_totales - 1

                                # ---------------------------- Acumulador de Festivos----------
                                # --------------------------------
                            elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                                # ---------------------------- Acumulador de Extras Festivos
                                # --------------------------------
                                if minutos_totales > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                                    else:
                                        minutos_extras_diurnos_festivo = minutos_extras_diurnos_festivo + 1
                                else:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                                    else:
                                        minutos_diurnos_festivo = minutos_diurnos_festivo + 1

                            # ---------------------------- Acumulador de Diurnos Normales -----------------------------
                            else:
                                # ---------------------------- Acumulador de  Extras Normales
                                # --------------------------------
                                if minutos_totales > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                                    else:
                                        minutos_extras_diurnos = minutos_extras_diurnos + 1
                                else:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_nocturnos = minutos_nocturnos + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_nocturnos = minutos_nocturnos + 1
                                    else:
                                        minutos_diurnos = minutos_diurnos + 1

                        self.total_horas = round(minutos_totales / 60, 1)
                        self.diurnas_totales = round(minutos_diurnos / 60, 1)
                        self.nocturnas_totales = round(
                            minutos_nocturnos / 60, 1)
                        self.extras_diurnas_totales = round(
                            minutos_extras_diurnos / 60, 1)
                        self.extras_nocturnos_totales = round(
                            minutos_extras_nocturnos / 60, 1)
                        self.diurnos_festivo_totales = round(
                            minutos_diurnos_festivo / 60, 1)
                        self.nocturnos_festivo_totales = round(
                            minutos_nocturnos_festivo / 60, 1)
                        self.extras_diurnos_festivo_totales = round(
                            minutos_extras_diurnos_festivo / 60, 1)
                        self.extras_nocturnos_festivo_totales = round(
                            minutos_extras_nocturnos_festivo / 60, 1)

                # ----------------------------- Función Jornada Continua sin descanso  -----------------------------
                def jornada_sin_descanso():
                    # --------------- Jornada con Dia diferente ------------------------------------------
                    if inicio_dia != salida_dia:
                        # -----------------------------------------------Día 1 ------ Acumuladores
                        minutos_diurnos_dia1 = 0
                        minutos_nocturnos_dia1 = 0
                        minutos_totales_dia1 = 0
                        minutos_extras_diurnos_dia1 = 0
                        minutos_extras_nocturnos_dia1 = 0
                        minutos_diurnos_festivo_dia1 = 0
                        minutos_nocturnos_festivo_dia1 = 0
                        minutos_extras_diurnos_festivo_dia1 = 0
                        minutos_extras_nocturnos_festivo_dia1 = 0
                        diurno1 = datetime(
                            inicio_year, inicio_mes, inicio_dia, 6, 0)
                        nocturno1 = datetime(
                            inicio_year, inicio_mes, inicio_dia, 21, 00)
                        salida_jornada = datetime(
                            salida_year, salida_mes, salida_dia, 0, 0)
                        while self.inicio_jornada_global <= salida_jornada:
                            self.inicio_jornada_global += timedelta(minutes=1)
                            minutos_totales_dia1 = minutos_totales_dia1 + 1
                            if inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                                if minutos_totales_dia1 > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                                    else:
                                        minutos_extras_diurnos_festivo_dia1 = minutos_extras_diurnos_festivo_dia1 + 1
                                else:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                                    else:
                                        minutos_diurnos_festivo_dia1 = minutos_diurnos_festivo_dia1 + 1
                            # ---------------------------- Acumulador de Extras día 1 --------------------------------
                            else:
                                if minutos_totales_dia1 > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                                    else:
                                        minutos_extras_diurnos_dia1 = minutos_extras_diurnos_dia1 + 1
                                else:
                                    if self.inicio_jornada_global < diurno1:
                                        minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                                    elif self.inicio_jornada_global > nocturno1:
                                        minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                                    else:
                                        minutos_diurnos_dia1 = minutos_diurnos_dia1 + 1

                        # # ------------------------- Acumulador de Extras día 2 o más --------------------------------
                        consolidado_minutos = minutos_totales_dia1
                        minutos_diurnos_dia2 = 0
                        minutos_nocturnos_dia2 = 0
                        minutos_totales_dia2 = 0
                        minutos_extras_diurnos_dia2 = 0
                        minutos_extras_nocturnos_dia2 = 0
                        minutos_diurnos_festivo_dia2 = 0
                        minutos_nocturnos_festivo_dia2 = 0
                        minutos_extras_diurnos_festivo_dia2 = 0
                        minutos_extras_nocturnos_festivo_dia2 = 0
                        diurno2 = datetime(
                            salida_year, salida_mes, salida_dia, 6, 0)
                        nocturno2 = datetime(
                            salida_year, salida_mes, salida_dia, 21, 00)
                        inicio_jornada2 = datetime(
                            salida_year, salida_mes, salida_dia, 0, 0)
                        salida_jornada2 = self.salida_jornada_global
                        inicio_dia_semana2 = inicio_jornada2.strftime("%A")
                        while inicio_jornada2 <= salida_jornada2:
                            inicio_jornada2 += timedelta(minutes=1)
                            minutos_totales_dia2 = minutos_totales_dia2 + 1
                            consolidado2 = consolidado_minutos + minutos_totales_dia2
                            if inicio_dia_semana2 == "domingo" or festivo_salida == "festivo":
                                if consolidado2 > jornada_legal_minutos:
                                    if inicio_jornada2 < diurno2:
                                        minutos_extras_nocturnos_festivo_dia2 = \
                                            minutos_extras_nocturnos_festivo_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_extras_nocturnos_festivo_dia2 = minutos_extras_nocturnos_festivo_dia2 + 1
                                    else:
                                        minutos_extras_diurnos_festivo_dia2 = minutos_extras_diurnos_festivo_dia2 + 1
                                else:
                                    if inicio_jornada2 < diurno2:
                                        minutos_nocturnos_festivo_dia2 = minutos_nocturnos_festivo_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_nocturnos_festivo_dia2 = minutos_nocturnos_festivo_dia2 + 1
                                    else:
                                        minutos_diurnos_festivo_dia2 = minutos_diurnos_festivo_dia2 + 1
                            else:
                                if consolidado2 > jornada_legal_minutos:
                                    if inicio_jornada2 < diurno2:
                                        minutos_extras_nocturnos_dia2 = minutos_extras_nocturnos_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_extras_nocturnos_dia2 = minutos_extras_nocturnos_dia2 + 1
                                    else:
                                        minutos_extras_diurnos_dia2 = minutos_extras_diurnos_dia2 + 1
                                else:
                                    if inicio_jornada2 < diurno2:
                                        minutos_nocturnos_dia2 = minutos_nocturnos_dia2 + 1
                                    elif inicio_jornada2 > nocturno2:
                                        minutos_nocturnos_dia2 = minutos_nocturnos_dia2 + 1
                                    else:
                                        minutos_diurnos_dia2 = minutos_diurnos_dia2 + 1
                        self.total_horas = round(
                            (minutos_totales_dia2 + consolidado_minutos) / 60, 1)
                        self.diurnas_totales = round(
                            (minutos_diurnos_dia1 + minutos_diurnos_dia2) / 60, 1)
                        self.nocturnas_totales = round(
                            (minutos_nocturnos_dia1 + minutos_nocturnos_dia2) / 60, 1)
                        self.extras_diurnas_totales = round(
                            (minutos_extras_diurnos_dia1 +
                             minutos_extras_diurnos_dia2) / 60,
                            1)
                        self.extras_nocturnos_totales = round(
                            (minutos_extras_nocturnos_dia1 + minutos_extras_nocturnos_dia2) / 60, 1)
                        self.diurnos_festivo_totales = round(
                            (minutos_diurnos_festivo_dia1 +
                             minutos_diurnos_festivo_dia2) / 60,
                            1)
                        self.nocturnos_festivo_totales = round(
                            (minutos_nocturnos_festivo_dia1 + minutos_nocturnos_festivo_dia2) / 60, 1)
                        self.extras_diurnos_festivo_totales = round(
                            (minutos_extras_diurnos_festivo_dia1 + minutos_extras_diurnos_festivo_dia2) / 60, 1)
                        self.extras_nocturnos_festivo_totales = round(
                            (minutos_extras_nocturnos_festivo_dia1 + minutos_extras_nocturnos_festivo_dia2) / 60, 1)
                        # ------------------------------------- Jornada mismo día-------------------------------------
                    else:
                        diurno = datetime(
                            inicio_year, inicio_mes, inicio_dia, 6, 0)
                        nocturno = datetime(
                            inicio_year, inicio_mes, inicio_dia, 21, 00)
                        minutos_totales = -1
                        minutos_diurnos = 0
                        minutos_nocturnos = 0
                        minutos_extras_diurnos = 0
                        minutos_extras_nocturnos = 0
                        minutos_diurnos_festivo = 0
                        minutos_nocturnos_festivo = 0
                        minutos_extras_diurnos_festivo = 0
                        minutos_extras_nocturnos_festivo = 0
                        while self.inicio_jornada_global <= self.salida_jornada_global:
                            self.inicio_jornada_global += timedelta(minutes=1)
                            minutos_totales = minutos_totales + 1
                            # ---------------------------- Acumulador de Festivos-------------------------------------
                            if inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                                # ------------------ Acumulador de Extras Festivos ---------------------------
                                if minutos_totales > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                                    else:
                                        minutos_extras_diurnos_festivo = minutos_extras_diurnos_festivo + 1
                                else:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                                    else:
                                        minutos_diurnos_festivo = minutos_diurnos_festivo + 1
                            # ---------------------------- Acumulador de Diurnos Normales -----------------------------
                            else:
                                # ---------------------------- Acumulador de  Extras Normales
                                if minutos_totales > jornada_legal_minutos:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                                    else:
                                        minutos_extras_diurnos = minutos_extras_diurnos + 1
                                else:
                                    if self.inicio_jornada_global < diurno:
                                        minutos_nocturnos = minutos_nocturnos + 1
                                    elif self.inicio_jornada_global > nocturno:
                                        minutos_nocturnos = minutos_nocturnos + 1
                                    else:
                                        minutos_diurnos = minutos_diurnos + 1
                        self.total_horas = round(minutos_totales / 60, 2)
                        self.diurnas_totales = round(minutos_diurnos / 60, 1)
                        self.nocturnas_totales = round(
                            minutos_nocturnos / 60, 1)
                        self.extras_diurnas_totales = round(
                            minutos_extras_diurnos / 60, 1)
                        self.extras_nocturnos_totales = round(
                            minutos_extras_nocturnos / 60, 1)
                        self.diurnos_festivo_totales = round(
                            minutos_diurnos_festivo / 60, 1)
                        self.nocturnos_festivo_totales = round(
                            minutos_nocturnos_festivo / 60, 2)
                        self.extras_diurnos_festivo_totales = round(
                            minutos_extras_diurnos_festivo / 60, 1)
                        self.extras_nocturnos_festivo_totales = round(
                            minutos_extras_nocturnos_festivo / 60, 1)

                if self.inicio_descanso_global is None and self.salida_descanso_global is None:
                    jornada_sin_descanso()
                elif self.inicio_descanso_global2 is None and self.salida_descanso_global2 is None:
                    jornada_un_descanso()
                else:
                    jornada_dos_descansos()

            calculohoras()

        enteros()
