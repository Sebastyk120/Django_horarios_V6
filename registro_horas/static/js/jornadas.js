let dataTable;
let dataTableInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {
            className: "centered",
            targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        },
        {orderable: false, targets: [20, 21]},
        {searchable: false, targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21]}
    ],
    pageLength: 10,
    destroy: true
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
                    <td>${todas_jornadas.empleado_nombre}</td>
                    <td>${todas_jornadas.user_id}</td>
                    <td>${todas_jornadas.total_horas > 10
                ? "<i class='fa-solid fa-xmark' style ='color: red;'></i>"
                : "<i class='fa-solid fa check' style ='color: green;'></i>"}</td>
                    <td>
                    <a href="actualizar/${todas_jornadas.id}/"> <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil' id="Editar"></i></button></a>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></button>
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