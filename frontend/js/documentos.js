const tablaDocumentos = document.getElementById("tabla-documentos");

Promise.all([
    fetchConToken(API_URL + "/documentos").then(function(r) { return r.json(); }),
    fetchConToken(API_URL + "/choferes").then(function(r) { return r.json(); })
])
.then(function(resultados) {
    const documentos = resultados[0];
    const choferes = resultados[1];

    const nombresPorId = {};
    choferes.forEach(function(chofer) {
        nombresPorId[chofer.id] = [chofer.nombre, chofer.ap_paterno, chofer.ap_materno].filter(Boolean).join(" ");
    });

    documentos.forEach(function(doc) {
        const fila = document.createElement("tr");
        const nombreChofer = nombresPorId[doc.chofer_id] || ("Chofer " + doc.chofer_id);

        fila.innerHTML = `
            <td></td>
            <td></td>
            <td></td>
            <td><a href="${API_URL}/uploads/${encodeURIComponent(doc.archivo)}" target="_blank">Ver archivo</a></td>
            <td><button type="button" class="btn-delete">Eliminar</button></td>
        `;

        fila.cells[0].textContent = nombreChofer;
        fila.cells[1].textContent = doc.tipo_documento || "";
        fila.cells[2].textContent = doc.fecha_subida || "";

        const botonEliminar = fila.querySelector("button");
        botonEliminar.addEventListener("click", function() {
            const confirmar = confirm("¿Eliminar este documento de " + nombreChofer + "?");
            if (!confirmar) return;

            fetchConToken(API_URL + "/documentos/" + doc.id, { method: "DELETE" })
                .then(function(respuesta) { return respuesta.json(); })
                .then(function() { fila.remove(); });
        });

        tablaDocumentos.appendChild(fila);
    });
})
.catch(function(error) {
    console.error(error);
    tablaDocumentos.innerHTML = `
        <tr><td colspan="5">No se pudieron cargar los documentos.</td></tr>
    `;
});
