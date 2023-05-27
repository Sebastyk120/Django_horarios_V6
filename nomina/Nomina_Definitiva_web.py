from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_ALL, ("esp", "UTF-8"))

inicio_jornada_globalf = "2023-01-20 06:00"
salida_jornada_globalf = "2023-01-20 20:00"
inicio_descanso_globalf = "2023-01-20 13:00"
salida_descanso_globalf = "2023-01-20 14:00"
inicio_descanso_global2f = "2023-01-20 15:00"
salida_descanso_global2f = "2023-01-20 16:00"
formato = "%Y-%m-%d %H:%M"
jornada_legal = 8
inicio_jornada_global = datetime.strptime(inicio_jornada_globalf, formato)
salida_jornada_global = datetime.strptime(salida_jornada_globalf, formato)
inicio_descanso_global = datetime.strptime(inicio_descanso_globalf, formato)
salida_descanso_global = datetime.strptime(salida_descanso_globalf, formato)
inicio_descanso_global2 = datetime.strptime(inicio_descanso_global2f, formato)
salida_descanso_global2 = datetime.strptime(salida_descanso_global2f, formato)

# ---------------------- Enteros de fecha de entrada y salida ----------------------------------------
inicio_dia_semana = datetime.strftime(inicio_jornada_global, "%A")
inicio_year = int(datetime.strftime(inicio_jornada_global, "%Y"))
inicio_mes = int(datetime.strftime(inicio_jornada_global, "%m"))
inicio_dia = int(datetime.strftime(inicio_jornada_global, "%d"))
salida_dia_semana = datetime.strftime(salida_jornada_global, "%A")
salida_year = int(datetime.strftime(salida_jornada_global, "%Y"))
salida_mes = int(datetime.strftime(salida_jornada_global, "%m"))
salida_dia = int(datetime.strftime(salida_jornada_global, "%d"))
jornada_legal_minutos = jornada_legal * 60


# ----------------- Horas y fechas de jornada --------------------------------------------
def calculohoras():
    # ------------------------------------Lista De Festivos Colombia 2023 -------------------------------
    def festivos():
        inicio_jornada_global_festivo = datetime.strftime(inicio_jornada_global, "%Y/%m/%d")
        salida_jornada_global_festivo = datetime.strftime(salida_jornada_global, "%Y/%m/%d")
        festivos_lista = ["2023/01/01", "2023/01/09", "2023/03/20", "2023/04/02", "2023/04/06", "2023/04/07",
                          "2023/04/09",
                          "2023/05/01", "2023/05/22", "2023/06/12", "2023/06/19"]
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

    # -------------------------------Jornada Con Descanso ------------------------------
    def jornada_un_descanso():
        # --------------- Jornada con Dia diferente ------------------------------------------
        global inicio_jornada_global
        if inicio_dia != salida_dia:
            # ------------------------------------- Día 1 ----------------------------------------------------
            minutos_diurnos_dia1 = 0
            minutos_nocturnos_dia1 = 0
            minutos_totales_dia1 = 0
            minutos_extras_diurnos_dia1 = 0
            minutos_extras_nocturnos_dia1 = 0
            minutos_diurnos_festivo_dia1 = 0
            minutos_nocturnos_festivo_dia1 = 0
            minutos_extras_diurnos_festivo_dia1 = 0
            minutos_extras_nocturnos_festivo_dia1 = 0
            diurno1 = datetime(inicio_year, inicio_mes, inicio_dia, 6, 0)
            nocturno1 = datetime(inicio_year, inicio_mes, inicio_dia, 21, 00)
            salida_jornada = datetime(salida_year, salida_mes, salida_dia, 0, 0)
            while inicio_jornada_global <= salida_jornada:
                inicio_jornada_global += timedelta(minutes=1)
                minutos_totales_dia1 = minutos_totales_dia1 + 1
                # ------------------------------Acumulador de Descansos --------------------------------
                if inicio_descanso_global <= inicio_jornada_global <= salida_descanso_global:
                    inicio_jornada_global += timedelta(minutes=1)
                    minutos_totales_dia1 = minutos_totales_dia1 - 1
                    continue
                elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                    if minutos_totales_dia1 > jornada_legal_minutos:
                        if inicio_jornada_global < diurno1:
                            minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                        else:
                            minutos_extras_diurnos_festivo_dia1 = minutos_extras_diurnos_festivo_dia1 + 1
                    else:
                        if inicio_jornada_global < diurno1:
                            minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                        else:
                            minutos_diurnos_festivo_dia1 = minutos_diurnos_festivo_dia1 + 1
                # ---------------------------- Acumulador de Extras día 1 --------------------------------
                else:
                    if minutos_totales_dia1 > jornada_legal_minutos:
                        if inicio_jornada_global < diurno1:
                            minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                        else:
                            minutos_extras_diurnos_dia1 = minutos_extras_diurnos_dia1 + 1
                    else:
                        if inicio_jornada_global < diurno1:
                            minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                        else:
                            minutos_diurnos_dia1 = minutos_diurnos_dia1 + 1

            # # ---------------------------- Acumulador de Extras día 2 o más --------------------------------
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
            diurno2 = datetime(salida_year, salida_mes, salida_dia, 6, 0)
            nocturno2 = datetime(salida_year, salida_mes, salida_dia, 21, 00)
            inicio_jornada2 = datetime(salida_year, salida_mes, salida_dia, 0, 0)
            salida_jornada2 = salida_jornada_global
            inicio_dia_semana2 = inicio_jornada2.strftime("%A")
            while inicio_jornada2 <= salida_jornada2:
                inicio_jornada2 += timedelta(minutes=1)
                minutos_totales_dia2 = minutos_totales_dia2 + 1
                consolidado2 = consolidado_minutos + minutos_totales_dia2
                # ------------------------------Acumulador de Descansos --------------------------------
                if inicio_descanso_global <= inicio_jornada2 <= salida_descanso_global:
                    inicio_jornada2 += timedelta(minutes=1)
                    minutos_totales_dia2 = minutos_totales_dia2 - 1
                    continue
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
            total_horas = round((minutos_totales_dia2 + consolidado_minutos) / 60, 1)
            diurnas_totales = round((minutos_diurnos_dia1 + minutos_diurnos_dia2) / 60, 1)
            nocturnas_totales = round((minutos_nocturnos_dia1 + minutos_nocturnos_dia2) / 60, 1)
            extras_diurnas_totales = round((minutos_extras_diurnos_dia1 + minutos_extras_diurnos_dia2) / 60, 1)
            extras_nocturnos_totales = round((minutos_extras_nocturnos_dia1 + minutos_extras_nocturnos_dia2) / 60, 1)
            diurnos_festivo_totales = round((minutos_diurnos_festivo_dia1 + minutos_diurnos_festivo_dia2) / 60, 1)
            nocturnos_festivo_totales = round((minutos_nocturnos_festivo_dia1 + minutos_nocturnos_festivo_dia2) / 60, 1)
            extras_diurnos_festivo_totales = round(
                (minutos_extras_diurnos_festivo_dia1 + minutos_extras_diurnos_festivo_dia2) / 60, 1)
            extras_nocturnos_festivo_totales = round(
                (minutos_extras_nocturnos_festivo_dia1 + minutos_extras_nocturnos_festivo_dia2) / 60, 1)
            print(f"Horas Totales: {total_horas}\n"
                  f"Horas diurnas: {diurnas_totales}\n"
                  f"Horas Nocturnas: {nocturnas_totales}\n"
                  f"Extras Diurnas: {extras_diurnas_totales}\n"
                  f"Extras Nocturnas: {extras_nocturnos_totales}\n"
                  f"Horas Diurnas Festivas: {diurnos_festivo_totales}\n"
                  f"Horas Nocturnas Festivas: {nocturnos_festivo_totales}\n"
                  f"Horas Extras Diurnas Festivas: {extras_diurnos_festivo_totales}\n"
                  f"Horas Extras Nocturnas Festivas: {extras_nocturnos_festivo_totales}")

        # ------------------------------------- Jornada mismo día  ----------------------------------------------------

        else:
            diurno = datetime(inicio_year, inicio_mes, inicio_dia, 6, 0)
            nocturno = datetime(inicio_year, inicio_mes, inicio_dia, 21, 00)
            minutos_totales = 0
            minutos_diurnos = 0
            minutos_nocturnos = 0
            minutos_extras_diurnos = 0
            minutos_extras_nocturnos = 0
            minutos_diurnos_festivo = 0
            minutos_nocturnos_festivo = 0
            minutos_extras_diurnos_festivo = 0
            minutos_extras_nocturnos_festivo = 0
            while inicio_jornada_global <= salida_jornada_global:
                inicio_jornada_global += timedelta(minutes=1)
                minutos_totales = minutos_totales + 1
                # ------------------------------Acumulador de Descansos --------------------------------
                if inicio_descanso_global <= inicio_jornada_global <= salida_descanso_global:
                    inicio_jornada_global += timedelta(minutes=1)
                    minutos_totales = minutos_totales - 1
                    continue
                    # ---------------------------- Acumulador de Festivos---------- --------------------------------
                elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                    # ---------------------------- Acumulador de Extras Festivos --------------------------------
                    if minutos_totales > jornada_legal_minutos:
                        if inicio_jornada_global < diurno:
                            minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                        else:
                            minutos_extras_diurnos_festivo = minutos_extras_diurnos_festivo + 1
                    else:
                        if inicio_jornada_global < diurno:
                            minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                        else:
                            minutos_diurnos_festivo = minutos_diurnos_festivo + 1

                # ---------------------------- Acumulador de Diurnos Normales --------------------------------
                else:
                    # ---------------------------- Acumulador de  Extras Normales --------------------------------
                    if minutos_totales > jornada_legal_minutos:
                        if inicio_jornada_global < diurno:
                            minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                        else:
                            minutos_extras_diurnos = minutos_extras_diurnos + 1
                    else:
                        if inicio_jornada_global < diurno:
                            minutos_nocturnos = minutos_nocturnos + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_nocturnos = minutos_nocturnos + 1
                        else:
                            minutos_diurnos = minutos_diurnos + 1

            total_horas = round(minutos_totales / 60, 1)
            diurnas_totales = round(minutos_diurnos / 60, 1)
            nocturnas_totales = round(minutos_nocturnos / 60, 1)
            extras_diurnas_totales = round(minutos_extras_diurnos / 60, 1)
            extras_nocturnos_totales = round(minutos_extras_nocturnos / 60, 1)
            diurnos_festivo_totales = round(minutos_diurnos_festivo / 60, 1)
            nocturnos_festivo_totales = round(minutos_nocturnos_festivo / 60, 1)
            extras_diurnos_festivo_totales = round(minutos_extras_diurnos_festivo / 60, 1)
            extras_nocturnos_festivo_totales = round(minutos_extras_nocturnos_festivo / 60, 1)
            print(f"Horas Totales: {total_horas}\n"
                  f"Horas diurnas: {diurnas_totales}\n"
                  f"Horas Nocturnas: {nocturnas_totales}\n"
                  f"Extras Diurnas: {extras_diurnas_totales}\n"
                  f"Extras Nocturnas: {extras_nocturnos_totales}\n"
                  f"Horas Diurnas Festivas: {diurnos_festivo_totales}\n"
                  f"Horas Nocturnas Festivas: {nocturnos_festivo_totales}\n"
                  f"Horas Extras Diurnas Festivas: {extras_diurnos_festivo_totales}\n"
                  f"Horas Extras Nocturnas Festivas: {extras_nocturnos_festivo_totales}")

    # -----------------------------------------------Jornada Con dos descansos-----------------------------------------
    def jornada_dos_descansos():
        global inicio_jornada_global
        # --------------- Jornada con Dia diferente ------------------------------------------
        if inicio_dia != salida_dia:
            # ------------------------------------- Día 1 ----------------------------------------------------
            minutos_diurnos_dia1 = 0
            minutos_nocturnos_dia1 = 0
            minutos_totales_dia1 = 0
            minutos_extras_diurnos_dia1 = 0
            minutos_extras_nocturnos_dia1 = 0
            minutos_diurnos_festivo_dia1 = 0
            minutos_nocturnos_festivo_dia1 = 0
            minutos_extras_diurnos_festivo_dia1 = 0
            minutos_extras_nocturnos_festivo_dia1 = 0
            diurno1 = datetime(inicio_year, inicio_mes, inicio_dia, 6, 0)
            nocturno1 = datetime(inicio_year, inicio_mes, inicio_dia, 21, 00)
            salida_jornada = datetime(salida_year, salida_mes, salida_dia, 0, 0)
            while inicio_jornada_global <= salida_jornada:
                inicio_jornada_global += timedelta(minutes=1)
                minutos_totales_dia1 = minutos_totales_dia1 + 1
                # ------------------------------Acumulador de Descansos --------------------------------
                if inicio_descanso_global <= inicio_jornada_global <= salida_descanso_global or \
                        inicio_descanso_global2 <= inicio_jornada_global <= salida_descanso_global2:
                    inicio_jornada_global += timedelta(minutes=1)
                    minutos_totales_dia1 = minutos_totales_dia1 - 1
                    continue
                elif inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                    if minutos_totales_dia1 > jornada_legal_minutos:
                        if inicio_jornada_global < diurno1:
                            minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                        else:
                            minutos_extras_diurnos_festivo_dia1 = minutos_extras_diurnos_festivo_dia1 + 1
                    else:
                        if inicio_jornada_global < diurno1:
                            minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                        else:
                            minutos_diurnos_festivo_dia1 = minutos_diurnos_festivo_dia1 + 1
                # ---------------------------- Acumulador de Extras día 1 --------------------------------
                else:
                    if minutos_totales_dia1 > jornada_legal_minutos:
                        if inicio_jornada_global < diurno1:
                            minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                        else:
                            minutos_extras_diurnos_dia1 = minutos_extras_diurnos_dia1 + 1
                    else:
                        if inicio_jornada_global < diurno1:
                            minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                        else:
                            minutos_diurnos_dia1 = minutos_diurnos_dia1 + 1

            # # ---------------------------- Acumulador de Extras día 2 o más --------------------------------
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
            diurno2 = datetime(salida_year, salida_mes, salida_dia, 6, 0)
            nocturno2 = datetime(salida_year, salida_mes, salida_dia, 21, 00)
            inicio_jornada2 = datetime(salida_year, salida_mes, salida_dia, 0, 0)
            salida_jornada2 = salida_jornada_global
            inicio_dia_semana2 = inicio_jornada2.strftime("%A")
            while inicio_jornada2 <= salida_jornada2:
                inicio_jornada2 += timedelta(minutes=1)
                minutos_totales_dia2 = minutos_totales_dia2 + 1
                consolidado2 = consolidado_minutos + minutos_totales_dia2
                # ------------------------------Acumulador de Descansos --------------------------------
                if inicio_descanso_global <= inicio_jornada2 <= salida_descanso_global or \
                        inicio_descanso_global2 <= inicio_jornada2 <= salida_descanso_global2:
                    inicio_jornada2 += timedelta(minutes=1)
                    minutos_totales_dia2 = minutos_totales_dia2 - 1
                    continue
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
            total_horas = round((minutos_totales_dia2 + consolidado_minutos) / 60, 1)
            diurnas_totales = round((minutos_diurnos_dia1 + minutos_diurnos_dia2) / 60, 1)
            nocturnas_totales = round((minutos_nocturnos_dia1 + minutos_nocturnos_dia2) / 60, 1)
            extras_diurnas_totales = round((minutos_extras_diurnos_dia1 + minutos_extras_diurnos_dia2) / 60, 1)
            extras_nocturnos_totales = round((minutos_extras_nocturnos_dia1 + minutos_extras_nocturnos_dia2) / 60, 1)
            diurnos_festivo_totales = round((minutos_diurnos_festivo_dia1 + minutos_diurnos_festivo_dia2) / 60, 1)
            nocturnos_festivo_totales = round((minutos_nocturnos_festivo_dia1 + minutos_nocturnos_festivo_dia2) / 60, 1)
            extras_diurnos_festivo_totales = round(
                (minutos_extras_diurnos_festivo_dia1 + minutos_extras_diurnos_festivo_dia2) / 60, 1)
            extras_nocturnos_festivo_totales = round(
                (minutos_extras_nocturnos_festivo_dia1 + minutos_extras_nocturnos_festivo_dia2) / 60, 1)
            print(f"Horas Totales: {total_horas}\n"
                  f"Horas diurnas: {diurnas_totales}\n"
                  f"Horas Nocturnas: {nocturnas_totales}\n"
                  f"Extras Diurnas: {extras_diurnas_totales}\n"
                  f"Extras Nocturnas: {extras_nocturnos_totales}\n"
                  f"Horas Diurnas Festivas: {diurnos_festivo_totales}\n"
                  f"Horas Nocturnas Festivas: {nocturnos_festivo_totales}\n"
                  f"Horas Extras Diurnas Festivas: {extras_diurnos_festivo_totales}\n"
                  f"Horas Extras Nocturnas Festivas: {extras_nocturnos_festivo_totales}")
            print("Dos Descansos")

    # ----------------------------- Función Jornada Continua sin descanso ---------------------------------------------
    def jornada_sin_descanso():
        global inicio_jornada_global
        # --------------- Jornada con Dia diferente ------------------------------------------
        if inicio_dia != salida_dia:
            # -----------------------------------------------Día 1 ----------------------------------------------------
            # ----------------------------------------- Inician acumuladores ----------------------------------
            minutos_diurnos_dia1 = 0
            minutos_nocturnos_dia1 = 0
            minutos_totales_dia1 = 0
            minutos_extras_diurnos_dia1 = 0
            minutos_extras_nocturnos_dia1 = 0
            minutos_diurnos_festivo_dia1 = 0
            minutos_nocturnos_festivo_dia1 = 0
            minutos_extras_diurnos_festivo_dia1 = 0
            minutos_extras_nocturnos_festivo_dia1 = 0
            diurno1 = datetime(inicio_year, inicio_mes, inicio_dia, 6, 0)
            nocturno1 = datetime(inicio_year, inicio_mes, inicio_dia, 21, 00)
            salida_jornada = datetime(salida_year, salida_mes, salida_dia, 0, 0)
            while inicio_jornada_global <= salida_jornada:
                inicio_jornada_global += timedelta(minutes=1)
                minutos_totales_dia1 = minutos_totales_dia1 + 1
                if inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                    if minutos_totales_dia1 > jornada_legal_minutos:
                        if inicio_jornada_global < diurno1:
                            minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_extras_nocturnos_festivo_dia1 = minutos_extras_nocturnos_festivo_dia1 + 1
                        else:
                            minutos_extras_diurnos_festivo_dia1 = minutos_extras_diurnos_festivo_dia1 + 1
                    else:
                        if inicio_jornada_global < diurno1:
                            minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_nocturnos_festivo_dia1 = minutos_nocturnos_festivo_dia1 + 1
                        else:
                            minutos_diurnos_festivo_dia1 = minutos_diurnos_festivo_dia1 + 1
                # ---------------------------- Acumulador de Extras día 1 --------------------------------
                else:
                    if minutos_totales_dia1 > jornada_legal_minutos:
                        if inicio_jornada_global < diurno1:
                            minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_extras_nocturnos_dia1 = minutos_extras_nocturnos_dia1 + 1
                        else:
                            minutos_extras_diurnos_dia1 = minutos_extras_diurnos_dia1 + 1
                    else:
                        if inicio_jornada_global < diurno1:
                            minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                        elif inicio_jornada_global > nocturno1:
                            minutos_nocturnos_dia1 = minutos_nocturnos_dia1 + 1
                        else:
                            minutos_diurnos_dia1 = minutos_diurnos_dia1 + 1

            # # ---------------------------- Acumulador de Extras día 2 o más --------------------------------
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
            diurno2 = datetime(salida_year, salida_mes, salida_dia, 6, 0)
            nocturno2 = datetime(salida_year, salida_mes, salida_dia, 21, 00)
            inicio_jornada2 = datetime(salida_year, salida_mes, salida_dia, 0, 0)
            salida_jornada2 = salida_jornada_global
            inicio_dia_semana2 = inicio_jornada2.strftime("%A")
            while inicio_jornada2 <= salida_jornada2:
                inicio_jornada2 += timedelta(minutes=1)
                minutos_totales_dia2 = minutos_totales_dia2 + 1
                consolidado2 = consolidado_minutos + minutos_totales_dia2
                if inicio_dia_semana2 == "domingo" or festivo_salida == "festivo":
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
            total_horas = round((minutos_totales_dia2 + consolidado_minutos) / 60, 1)
            diurnas_totales = round((minutos_diurnos_dia1 + minutos_diurnos_dia2) / 60, 1)
            nocturnas_totales = round((minutos_nocturnos_dia1 + minutos_nocturnos_dia2) / 60, 1)
            extras_diurnas_totales = round((minutos_extras_diurnos_dia1 + minutos_extras_diurnos_dia2) / 60, 1)
            extras_nocturnos_totales = round((minutos_extras_nocturnos_dia1 + minutos_extras_nocturnos_dia2) / 60, 1)
            diurnos_festivo_totales = round((minutos_diurnos_festivo_dia1 + minutos_diurnos_festivo_dia2) / 60, 1)
            nocturnos_festivo_totales = round((minutos_nocturnos_festivo_dia1 + minutos_nocturnos_festivo_dia2) / 60, 1)
            extras_diurnos_festivo_totales = round(
                (minutos_extras_diurnos_festivo_dia1 + minutos_extras_diurnos_festivo_dia2) / 60, 1)
            extras_nocturnos_festivo_totales = round(
                (minutos_extras_nocturnos_festivo_dia1 + minutos_extras_nocturnos_festivo_dia2) / 60, 1)
            print(f"Horas Totales: {total_horas}\n"
                  f"Horas diurnas: {diurnas_totales}\n"
                  f"Horas Nocturnas: {nocturnas_totales}\n"
                  f"Extras Diurnas: {extras_diurnas_totales}\n"
                  f"Extras Nocturnas: {extras_nocturnos_totales}\n"
                  f"Horas Diurnas Festivas: {diurnos_festivo_totales}\n"
                  f"Horas Nocturnas Festivas: {nocturnos_festivo_totales}\n"
                  f"Horas Extras Diurnas Festivas: {extras_diurnos_festivo_totales}\n"
                  f"Horas Extras Nocturnas Festivas: {extras_nocturnos_festivo_totales}")

        # ------------------------------------- Jornada mismo día  ----------------------------------------------------

        else:
            diurno = datetime(inicio_year, inicio_mes, inicio_dia, 6, 0)
            nocturno = datetime(inicio_year, inicio_mes, inicio_dia, 21, 00)
            minutos_totales = 0
            minutos_diurnos = 0
            minutos_nocturnos = 0
            minutos_extras_diurnos = 0
            minutos_extras_nocturnos = 0
            minutos_diurnos_festivo = 0
            minutos_nocturnos_festivo = 0
            minutos_extras_diurnos_festivo = 0
            minutos_extras_nocturnos_festivo = 0
            while inicio_jornada_global <= salida_jornada_global:
                inicio_jornada_global += timedelta(minutes=1)
                minutos_totales = minutos_totales + 1
                # ---------------------------- Acumulador de Festivos---------- --------------------------------
                if inicio_dia_semana == "domingo" or festivo_inicio == "festivo":
                    # ---------------------------- Acumulador de Extras Festivos --------------------------------
                    if minutos_totales > jornada_legal_minutos:
                        if inicio_jornada_global < diurno:
                            minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_extras_nocturnos_festivo = minutos_extras_nocturnos_festivo + 1
                        else:
                            minutos_extras_diurnos_festivo = minutos_extras_diurnos_festivo + 1
                    else:
                        if inicio_jornada_global < diurno:
                            minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_nocturnos_festivo = minutos_nocturnos_festivo + 1
                        else:
                            minutos_diurnos_festivo = minutos_diurnos_festivo + 1
                # ---------------------------- Acumulador de Diurnos Normales --------------------------------
                else:
                    # ---------------------------- Acumulador de  Extras Normales --------------------------------
                    if minutos_totales > jornada_legal_minutos:
                        if inicio_jornada_global < diurno:
                            minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_extras_nocturnos = minutos_extras_nocturnos + 1
                        else:
                            minutos_extras_diurnos = minutos_extras_diurnos + 1
                    else:
                        if inicio_jornada_global < diurno:
                            minutos_nocturnos = minutos_nocturnos + 1
                        elif inicio_jornada_global > nocturno:
                            minutos_nocturnos = minutos_nocturnos + 1
                        else:
                            minutos_diurnos = minutos_diurnos + 1
            total_horas = round(minutos_totales / 60, 1)
            diurnas_totales = round(minutos_diurnos / 60, 1)
            nocturnas_totales = round(minutos_nocturnos / 60, 1)
            extras_diurnas_totales = round(minutos_extras_diurnos / 60, 1)
            extras_nocturnos_totales = round(minutos_extras_nocturnos / 60, 1)
            diurnos_festivo_totales = round(minutos_diurnos_festivo / 60, 1)
            nocturnos_festivo_totales = round(minutos_nocturnos_festivo / 60, 1)
            extras_diurnos_festivo_totales = round(minutos_extras_diurnos_festivo / 60, 1)
            extras_nocturnos_festivo_totales = round(minutos_extras_nocturnos_festivo / 60, 1)
            print(f"Horas Totales: {total_horas}\n"
                  f"Horas diurnas: {diurnas_totales}\n"
                  f"Horas Nocturnas: {nocturnas_totales}\n"
                  f"Extras Diurnas: {extras_diurnas_totales}\n"
                  f"Extras Nocturnas: {extras_nocturnos_totales}\n"
                  f"Horas Diurnas Festivas: {diurnos_festivo_totales}\n"
                  f"Horas Nocturnas Festivas: {nocturnos_festivo_totales}\n"
                  f"Horas Extras Diurnas Festivas: {extras_diurnos_festivo_totales}\n"
                  f"Horas Extras Nocturnas Festivas: {extras_nocturnos_festivo_totales}")

    if inicio_descanso_global is None and salida_descanso_global is None:
        jornada_sin_descanso()
    elif inicio_descanso_global2 is None and salida_descanso_global2 is None:
        jornada_un_descanso()
    else:
        jornada_dos_descansos()


calculohoras()
