const dataTableOptions = {
  processing: true,
  processingIndicator: '<div class="loading-spinner"></div>',
  columnDefs: [
    {
      className: "centered",
      targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    },
    { orderable: false, targets: [7, 11] },
    { searchable: false, targets: [0, 4, 5, 6, 7, 8, 9, 10, 11] },
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
  try {
    const tableBody_empleados = document.querySelector("#tableBody_empleados");
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());
    const page = params.page || 1; // Si no hay valor para la página, se muestra la primera
    const data = await listempleados(page);
    const rows = data.todas_empleados.map(
      (todas_empleados, index) => `
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
      </tr>
    `
    );
    tableBody_empleados.innerHTML = rows.join("");
    const dataTable = $("#datatable_empleados").DataTable(dataTableOptions);
    $('.dataTables_filter input[type="search"]').addClass("form-control");
  } catch (ex) {
    console.error(ex);
    alert("Error al cargar los datos.");
  }
};

const listempleados = async (page) => {
  const response = await fetch(
    `http://127.0.0.1:8000/operaciones/lista/empleados/?page=${page}`
  );
  return response.json();
};

window.addEventListener("load", async () => {
  await initDatatable();
});