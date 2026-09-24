const API_URL = "http://127.0.0.1:5000";
const form = document.getElementById("chofer-form");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const datos = {
        nombre: document.getElementById("nombre").value,
        ap_paterno: document.getElementById("ap_paterno").value,
        ap_materno: document.getElementById("ap_materno").value,
        direccion: document.getElementById("direccion").value,
        telefono: document.getElementById("telefono").value,
        fecha_inicio: document.getElementById("fecha_inicio").value,
        reportado: document.getElementById("reportado").checked,
            };

fetch(API_URL + "/choferes", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(datos)
})
.then(function(respuesta) {
    return respuesta.json();
})
.then(function(resultado) {
    alert("Chofer creado con id: " + resultado.id);
});


});

