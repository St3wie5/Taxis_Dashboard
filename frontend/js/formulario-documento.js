const API_URL = "http://127.0.0.1:5000";
const form = document.getElementById("documento-form");
const selectChofer = document.getElementById("chofer_id");

fetch(API_URL + "/choferes")
    .then(function(respuesta) { return respuesta.json(); })
    .then(function(choferes) {
        choferes.forEach(function(chofer) {
            const nombreCompleto = [
                chofer.nombre,
                chofer.ap_paterno,
                chofer.ap_materno
            ].filter(Boolean).join(" ");

            const opcion = document.createElement("option");
            opcion.value = chofer.id;
            opcion.textContent = nombreCompleto || ("Chofer " + chofer.id);
            selectChofer.appendChild(opcion);
        });
    });

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const archivo = document.getElementById("archivo").files[0];
    if (!archivo) {
        mostrarMensaje("Selecciona un archivo", "error");
        return;
    }

    const datos = new FormData();
    datos.append("chofer_id", selectChofer.value);
    datos.append("tipo_documento", document.getElementById("tipo_documento").value);
    datos.append("archivo", archivo);

    fetch(API_URL + "/documentos/upload", {
        method: "POST",
        body: datos
    })
    .then(function(respuesta) {
        if (!respuesta.ok) {
            throw new Error("No se pudo subir el documento");
        }
        return respuesta.json();
    })
    .then(function() {
        mostrarMensaje("Documento subido correctamente");
        setTimeout(function () {
            window.location.href = "documentos.html";
        }, 900);
    })
    .catch(function(error) {
        console.error(error);
        mostrarMensaje("No se pudo subir el documento", "error");
    });
});
