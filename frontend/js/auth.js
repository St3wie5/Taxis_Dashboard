function obtenerToken() {
    return localStorage.getItem("sixat_token");
}

function guardarSesion(token, username, rol) {
    localStorage.setItem("sixat_token", token);
    localStorage.setItem("sixat_usuario", username);
    localStorage.setItem("sixat_rol", rol);
}

function cerrarSesion() {
    localStorage.removeItem("sixat_token");
    localStorage.removeItem("sixat_usuario");
    localStorage.removeItem("sixat_rol");
    window.location.href = "login.html";
}

function esAdmin() {
    return localStorage.getItem("sixat_rol") === "administrador";
}

function exigirSesion() {
    if (!obtenerToken()) {
        window.location.href = "login.html";
    }
}

function fetchConToken(url, opciones) {
    opciones = opciones || {};
    opciones.headers = Object.assign({}, opciones.headers, {
        "Authorization": "Bearer " + obtenerToken()
    });

    return fetch(url, opciones).then(function (respuesta) {
        if (respuesta.status === 401) {
            cerrarSesion();
            throw new Error("Sesion expirada");
        }
        return respuesta;
    });
}

exigirSesion();
