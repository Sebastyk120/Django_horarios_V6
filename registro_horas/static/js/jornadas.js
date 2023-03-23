let dataTable;
let dataTableInitialized = false;

const dataTableOptions = {
    processing: true,
    processingIndicator: '<div class="spinner"></div>',
    columnDefs: [
        {
            className: "centered",
            targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        },
        {orderable: false, targets: [21]},
        {searchable: false, targets: [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21]}
    ],
    paging: true,
    pageLength: 50,
    destroy: true,
    language: {
        search: "Buscar:",
        lengthMenu: "Mostrar _MENU_ registros",
        info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
        infoEmpty: "Mostrando 0 a 0 de 0 registros",
        infoFiltered: "(filtrado de _MAX_ registros en total)",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior",
        },
    },
};
const initDatatable = async () => {
    if (dataTableInitialized) {
        dataTable.destroy();
    }
    await listjornadas();
    dataTable = $('#datatable_jornadas').DataTable(dataTableOptions);

    dataTableInitialized = true;

};

const listjornadas = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/lista/jornadas/");
        const data = await response.json();
        let content = ``;
        data.todas_jornadas.forEach((todas_jornadas, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${todas_jornadas.empleado_nombre}</td>
                    <td>${todas_jornadas.empleado_cedula}</td>
                    <td>${todas_jornadas.inicio_jornada_global}</td>
                    <td>${todas_jornadas.salida_jornada_global}</td>
                    <td>${todas_jornadas.inicio_descanso_global}</td>
                    <td>${todas_jornadas.salida_descanso_global}</td>
                    <td>${todas_jornadas.inicio_descanso_global2}</td>
                    <td>${todas_jornadas.salida_descanso_global2}</td>
                    <td>${todas_jornadas.jornada_legal}</td>
                    <td>${todas_jornadas.total_horas}</td>
                    <td>${todas_jornadas.diurnas_totales}</td>
                    <td>${todas_jornadas.nocturnas_totales}</td>
                    <td>${todas_jornadas.extras_diurnas_totales}</td>
                    <td>${todas_jornadas.extras_nocturnos_totales}</td>
                    <td>${todas_jornadas.diurnos_festivo_totales}</td>
                    <td>${todas_jornadas.nocturnos_festivo_totales}</td>
                    <td>${todas_jornadas.extras_diurnos_festivo_totales}</td>
                    <td>${todas_jornadas.extras_nocturnos_festivo_totales}</td>
                    <td>${todas_jornadas.fh_transaccion}</td>            
                    <td>${todas_jornadas.user_id}</td>
                    <td>
                    <a href="actualizar/${todas_jornadas.id}/"> <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil' id="Editar"></i></button></a>
                    <a href="eliminar/${todas_jornadas.id}/">  <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can' id="Eliminar"></i></button></a>
                    </td>
                </tr>
            `;
        });
        tableBody_jornadas.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDatatable();
});