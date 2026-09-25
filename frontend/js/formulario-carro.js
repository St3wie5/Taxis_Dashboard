const params = new URLSearchParams(window.location.search);
const idEditar = params.get("id");
const form = document.getElementById("carro-form");
const inputId = document.getElementById("id");
const selectChofer = document.getElementById("chofer_id");
const campoChofer = document.getElementById("campo-chofer");

if (idEditar) {
    inputId.value = idEditar;
    inputId.disabled = true;
    campoChofer.style.display = "none";

    fetchConToken(API_URL + "/carros/" + idEditar)
        .then(function(respuesta) { return respuesta.json(); })
        .then(function(carro) {
            document.getElementById("marca").value = carro.marca;
            document.getElementById("modelo").value = carro.modelo;
            document.getElementById("anio").value = carro.anio;
            document.getElementById("placas").value = carro.placas;
            document.getElementById("serie").value = carro.serie;
            document.getElementById("motor").value = carro.motor;
            document.getElementById("duenio").value = carro.duenio;
            document.getElementById("estado").value = carro.estado;
        });
} else {
    fetchConToken(API_URL + "/choferes")
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
}

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const datos = {
        marca: document.getElementById("marca").value.trim().toUpperCase(),
        modelo: document.getElementById("modelo").value.trim().toUpperCase(),
        anio: document.getElementById("anio").value,
        placas: document.getElementById("placas").value.trim().toUpperCase(),
        serie: document.getElementById("serie").value.trim().toUpperCase(),
        motor: document.getElementById("motor").value.trim().toUpperCase(),
        duenio: document.getElementById("duenio").value.trim().toUpperCase(),
        estado: document.getElementById("estado").value,
    };

    const metodo = idEditar ? "PUT" : "POST";
    const url = idEditar ? API_URL + "/carros/" + idEditar : API_URL + "/carros";

    if (!idEditar) {
        datos.id = inputId.value.trim().toUpperCase();
    }

    fetchConToken(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
    .then(function(respuesta) { return respuesta.json(); })
    .then(function(resultado) {
        const choferSeleccionado = !idEditar ? selectChofer.value : "";

        if (choferSeleccionado) {
            return fetchConToken(API_URL + "/asignaciones", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    carro_id: resultado.id,
                    chofer_id: choferSeleccionado,
                    fecha_inicio: new Date().toISOString().split("T")[0]
                })
            }).then(function() {
                mostrarMensaje("Carro creado y chofer asignado");
            });
        }

        mostrarMensaje(idEditar ? "Carro actualizado" : "Carro creado con id: " + resultado.id);
    })
    .then(function() {
        setTimeout(function () {
            window.location.href = "carros.html";
        }, 900);
    });
});
