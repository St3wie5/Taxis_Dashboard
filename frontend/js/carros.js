const API_URL = "http://127.0.0.1:5000";
const tablaCarros = document.getElementById("tabla-carros");

fetch(API_URL + "/carros")
    .then(function(respuesta) {
        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los carros");
        }
        return respuesta.json();
    })
    .then(function(carros) {
        carros.forEach(function(carro) {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>
                    <a href="agregar-carro.html?id=${encodeURIComponent(carro.id)}" class="btn-edit">Editar</a>
                    <button type="button" class="btn-delete">Eliminar</button>
                </td>
            `;

            fila.cells[0].textContent = carro.id;
            fila.cells[1].textContent = carro.marca || "";
            fila.cells[2].textContent = carro.modelo || "";
            fila.cells[3].textContent = carro.placas || "";
            fila.cells[4].textContent = carro.estado || "";

            const botonEliminar = fila.querySelector("button");
            botonEliminar.addEventListener("click", function() {
                const confirmar = confirm("¿Seguro que quieres eliminar el carro " + carro.id + "?");
                if (!confirmar) return;

                fetch(API_URL + "/carros/" + carro.id, {
                    method: "DELETE"
                })
                .then(function(respuesta) {
                    return respuesta.json();
                })
                .then(function() {
                    fila.remove();
                });
            });

            tablaCarros.appendChild(fila);
        });
    })
    .catch(function(error) {
        console.error(error);
        tablaCarros.innerHTML = `
            <tr>
                <td colspan="6">No se pudieron cargar los carros.</td>
            </tr>
        `;
    });
