const dataTableOptions = {
  columnDefs: [
    {
      className: "centered",
      targets: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    },
  ],
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
          <td>
            <a href="actualizar/${todas_empleados.id}/">
              <button class='btn btn-sm btn-primary' data-toggle="modal" data-target="#updateModal">
                <i class='fa-solid fa-pencil' id="Editar"></i>
              </button>
            </a>
          </td>
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
    `http://127.0.0.1:8000/lista/empleados/?page=${page}`
  );
  return response.json();
};

window.addEventListener("load", async () => {
  await initDatatable();
});
