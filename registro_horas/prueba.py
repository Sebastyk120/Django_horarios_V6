import locale
from calc_horarios import Horarios
from datetime import datetime

locale.setlocale(locale.LC_ALL, ("esp", "UTF-8"))

inicio_jornada_globalf = datetime(2023, 3, 1, 22, 0)
salida_jornada_globalf = datetime(2023, 3, 2, 22, 0)
inicio_descanso_globalf = None #datetime(2023, 2, 19, 13, 00)
salida_descanso_globalf = None #datetime(2023, 2, 19, 14, 00)
inicio_descanso_global2f = None #datetime(2023, 2, 19, 14, 00)
salida_descanso_global2f = None #datetime(2023, 2, 19, 14, 00)
jornada_legalf = 8

horarioo = Horarios(inicio_jornada_globalf, salida_jornada_globalf, inicio_descanso_globalf, salida_descanso_globalf,
                    inicio_descanso_global2f, salida_descanso_global2f, jornada_legalf)

print(f"Horas Totales: {horarioo.total_horas}\n"
      f"Horas diurnas: {horarioo.diurnas_totales}\n"
      f"Horas Nocturnas: {horarioo.nocturnas_totales}\n"
      f"Extras Diurnas: {horarioo.extras_diurnas_totales}\n"
      f"Extras Nocturnas: {horarioo.extras_nocturnos_totales}\n"
      f"Horas Diurnas Festivas: {horarioo.diurnos_festivo_totales}\n"
      f"Horas Nocturnas Festivas: {horarioo.nocturnos_festivo_totales}\n"
      f"Horas Extras Diurnas Festivas: {horarioo.extras_diurnos_festivo_totales}\n"
      f"Horas Extras Nocturnas Festivas: {horarioo.extras_nocturnos_festivo_totales}")
