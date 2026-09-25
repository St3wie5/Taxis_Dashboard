const API_URL = "http://127.0.0.1:5000";
const params = new URLSearchParams(window.location.search);
const idEditar = params.get("id");
const form = document.getElementById("chofer-form");

function aTituloCapital(texto) {
    return texto
        .toLowerCase()
        .split(" ")
        .map(function (palabra) {
            if (!palabra) return palabra;
            return palabra.charAt(0).toUpperCase() + palabra.slice(1);
        })
        .join(" ");
}

if (idEditar) {
    fetch(API_URL + "/choferes/" + idEditar)
        .then(function(respuesta) { return respuesta.json(); })
        .then(function(chofer) {
            document.getElementById("nombre").value = chofer.nombre;
            document.getElementById("ap_paterno").value = chofer.ap_paterno;
            document.getElementById("ap_materno").value = chofer.ap_materno;
            document.getElementById("direccion").value = chofer.direccion;
            document.getElementById("telefono").value = chofer.telefono;
            document.getElementById("reportado").checked = chofer.reportado;
        });
}

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const datos = {
        nombre: aTituloCapital(document.getElementById("nombre").value.trim()),
        ap_paterno: aTituloCapital(document.getElementById("ap_paterno").value.trim()),
        ap_materno: aTituloCapital(document.getElementById("ap_materno").value.trim()),
        direccion: document.getElementById("direccion").value.trim().toUpperCase(),
        telefono: document.getElementById("telefono").value.trim(),
        fecha_inicio: document.getElementById("fecha_inicio").value,
        reportado: document.getElementById("reportado").checked,
    };

    const metodo = idEditar ? "PUT" : "POST";
    const url = idEditar ? API_URL + "/choferes/" + idEditar : API_URL + "/choferes";

    fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
    })
    .then(function(respuesta) { return respuesta.json(); })
    .then(function(resultado) {
        mostrarMensaje(idEditar ? "Chofer actualizado" : "Chofer creado con id: " + resultado.id);
        setTimeout(function () {
            window.location.href = "choferes.html";
        }, 900);
    });
});
