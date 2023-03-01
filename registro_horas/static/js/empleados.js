let dataTable;
let dataTableInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {
            className: "centered",
            targets: [0, 1, 2, 3, 4, 5, 6]
        },
        {orderable: false, targets: [6]},
        {searchable: false, targets: [0, 2, 4, 5, 6]}
    ],
    pageLength: 10,
    destroy: true
};
const initDatatable = async () => {
    if (dataTableInitialized) {
        dataTable.destroy();
    }
    await listempleados();
    dataTable = $('#datatable_empleados').DataTable(dataTableOptions);

    dataTableInitialized = true;

};

const listempleados = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/lista/empleados/");
        const data = await response.json();
        let content = ``;
        data.todas_empleados.forEach((todas_empleados, index) => {
            content += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${todas_empleados.nombre}</td>
                    <td>${todas_empleados.cedula}</td>
                    <td>${todas_empleados.empresa}</td>
                    <td>${todas_empleados.estado}</td>
                    <td>${todas_empleados.estado === 'Inactivo'
                ? "<i class='fa-solid fa-xmark' style ='color: red;'></i>"
                : "<i class='fa-solid fa-check' style ='color: green;'></i>"}</td>
                    <td>
                        <a href="actualizar/${todas_empleados.id}/"> <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil' id="Editar"></i></button></a>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can' id="Eliminar"></i></button>
                    </td>
                </tr>
            `;
        });
        tableBody_empleados.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDatatable();
});

