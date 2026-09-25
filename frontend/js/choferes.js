const tablaChoferes = document.getElementById("tabla-choferes");

fetchConToken(API_URL + "/choferes")
    .then(function(respuesta) {
        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los choferes");
        }
        return respuesta.json();
    })
    .then(function(choferes) {
        choferes.forEach(function(chofer) {
            const fila = document.createElement("tr");
            const nombre = [
                chofer.nombre,
                chofer.ap_paterno,
                chofer.ap_materno
            ].filter(Boolean).join(" ");

            fila.innerHTML = `
                <td></td>
                <td></td>
                <td></td>
                <td>
                    <a href="agregar-chofer.html?id=${encodeURIComponent(chofer.id)}" class="btn-edit">Editar</a>
                    <button type="button" class="btn-delete" data-id="${chofer.id}">Eliminar</button>
                </td>
            `;

            fila.cells[0].textContent = nombre || "Sin nombre";
            fila.cells[1].textContent = chofer.telefono || "No registrado";
            fila.cells[2].textContent = chofer.reportado ? "Sí" : "No";
            const botonEliminar = fila.querySelector("button");
            botonEliminar.addEventListener("click", function() {
                const confirmar = confirm("¿Seguro que quieres eliminar a " + nombre + "?");
                if (!confirmar) return;

                fetchConToken(API_URL + "/choferes/" + chofer.id, {
                    method: "DELETE"
                })
                .then(function(respuesta) {
                    return respuesta.json();
                })
                .then(function() {
                    fila.remove();
                });
            });
            
            tablaChoferes.appendChild(fila);
        });
    })
    .catch(function(error) {
        console.error(error);
        tablaChoferes.innerHTML = `
            <tr>
                <td colspan="4">No se pudieron cargar los choferes.</td>
            </tr>
        `;
    });