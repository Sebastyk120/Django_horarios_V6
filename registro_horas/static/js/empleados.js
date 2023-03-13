let dataTable;
let dataTableInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {
            className: "centered",
            targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        },
        {orderable: false, targets: [7, 11]},
        {searchable: false, targets: [0, 4, 5, 6, 7, 8, 9, 10, 11]}
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
                    <td>${todas_empleados.tdoc}</td>
                    <td>${todas_empleados.cedula}</td>
                    <td>${todas_empleados.empresa}</td>
                    <td>${todas_empleados.estado}</td>
                    <td>${todas_empleados.contrato}</td>
                    <td>${todas_empleados.area}</td>
                    <td>${todas_empleados.cargo}</td>
                    <td>${todas_empleados.salario}</td>
                    <td>${todas_empleados.generaextras}</td>
                    <td>${todas_empleados.ingreso}</td>
                    <td>${todas_empleados.retiro}</td>
                    <td>
                        <a href="actualizar/${todas_empleados.id}/"> <button class='btn btn-sm btn-primary data-toggle="modal" data-target="#updateModal"'><i class='fa-solid fa-pencil' id="Editar"></i></button></a>
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

