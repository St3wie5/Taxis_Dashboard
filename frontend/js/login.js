const form = document.getElementById("login-form");
const errorMsg = document.getElementById("login-error");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

    errorMsg.style.display = "none";

    if (usuario === "" || password === "") {
        errorMsg.textContent = "Escribe tu usuario y contrasena.";
        errorMsg.style.display = "block";
        return;
    }

    fetch(API_URL + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: usuario, password: password })
    })
    .then(function(respuesta) {
        return respuesta.json().then(function(datos) {
            return { ok: respuesta.ok, datos: datos };
        });
    })
    .then(function(resultado) {
        if (!resultado.ok) {
            errorMsg.textContent = resultado.datos.error || "Usuario o contrasena incorrectos.";
            errorMsg.style.display = "block";
            return;
        }

        guardarSesion(resultado.datos.token, resultado.datos.username, resultado.datos.rol);
        window.location.href = "dashboard.html";
    })
    .catch(function(error) {
        console.error(error);
        errorMsg.textContent = "No se pudo conectar con el servidor.";
        errorMsg.style.display = "block";
    });
});
