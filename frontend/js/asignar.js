const API_URL = "http://127.0.0.1:5000";
const selectCarro = document.getElementById("carro_id");
const selectChofer = document.getElementById("chofer_id");
const inputFecha = document.getElementById("fecha_inicio");
const form = document.getElementById("asignar-form");

const params = new URLSearchParams(window.location.search);
const carroPreseleccionado = params.get("carro_id");

inputFecha.value = new Date().toISOString().split("T")[0];

fetch(API_URL + "/carros")
    .then(function(respuesta) { return respuesta.json(); })
    .then(function(carros) {
        carros.forEach(function(carro) {
            const opcion = document.createElement("option");
            opcion.value = carro.id;
            opcion.textContent = carro.id + " - " + (carro.marca || "") + " " + (carro.modelo || "");
            selectCarro.appendChild(opcion);
        });
        if (carroPreseleccionado) {
            selectCarro.value = carroPreseleccionado;
        }
    });

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

    const datos = {
        carro_id: selectCarro.value,
        chofer_id: selectChofer.value,
        fecha_inicio: inputFecha.value
    };

    fetch(API_URL + "/asignaciones", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
    .then(function(respuesta) { return respuesta.json(); })
    .then(function() {
        mostrarMensaje("Chofer asignado al carro " + datos.carro_id);
        setTimeout(function () {
            window.location.href = "dashboard.html";
        }, 900);
    })
    .catch(function(error) {
        console.error(error);
        mostrarMensaje("No se pudo crear la asignación", "error");
    });
});
