const listJornadas = async (fechaInicio, fechaFin) => {
  try {
    let url = "http://127.0.0.1:8000/nomina/lista/jornadas/";
    if (fechaInicio && fechaFin) {
      url += `?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    // Obtén una referencia al DataTable
    const dataTable = $('#datatable_jornadas').DataTable();

    // Borra todas las filas existentes
    dataTable.clear().draw();

    // Agrega las nuevas filas al DataTable
    if (Array.isArray(data.todas_jornadas)) {
      data.todas_jornadas.forEach((todas_jornadas, index) => {
        dataTable.row.add([
          index + 1,
          todas_jornadas.empleado_nombre,
          todas_jornadas.empleado_cedula,
          todas_jornadas.inicio_jornada_global,
          todas_jornadas.salida_jornada_global,
          todas_jornadas.inicio_descanso_global,
          todas_jornadas.salida_descanso_global,
          todas_jornadas.inicio_descanso_global2,
          todas_jornadas.salida_descanso_global2,
          todas_jornadas.jornada_legal,
          todas_jornadas.total_horas,
          todas_jornadas.diurnas_totales,
          todas_jornadas.nocturnas_totales,
          todas_jornadas.extras_diurnas_totales,
          todas_jornadas.extras_nocturnos_totales,
          todas_jornadas.diurnos_festivo_totales,
          todas_jornadas.nocturnos_festivo_totales,
          todas_jornadas.extras_diurnos_festivo_totales,
          todas_jornadas.extras_nocturnos_festivo_totales,
          todas_jornadas.fh_transaccion,
          todas_jornadas.user_id,
          `
            <a href="actualizar/${todas_jornadas.id}/"><button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil' id="Editar"></i></button></a>
            <a href="eliminar/${todas_jornadas.id}/"><button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can' id="Eliminar"></i></button></a>
          `
        ]).draw(false);
      });
    } else {
      console.error("La propiedad todas_jornadas no es un array válido");
    }
  } catch (ex) {
    alert(ex);
  }
};

// Agrega un evento al botón de filtrar para obtener las fechas seleccionadas y actualizar la tabla
document.getElementById('filtrar-button').addEventListener('click', () => {
  const fechaInicio = document.getElementById('fecha-inicio').value;
  const fechaFin = document.getElementById('fecha-fin').value;
  listJornadas(fechaInicio, fechaFin);
});

$(document).ready(async function() {
  await initDatatable();
});
