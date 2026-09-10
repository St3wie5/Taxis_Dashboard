const form = document.getElementById("login-form");
const errorMsg = document.getElementById("login-error");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

    if (usuario === "" || password === "") {
        errorMsg.textContent = "Escribe tu usuario y contrasena.";
        errorMsg.style.display = "block";
        return;
    }

    // Por ahora no hay endpoint de login en el backend todavia.
    // Cuando lo construyan, aqui se hara un fetch POST a /login
    // enviando usuario y password, y solo se redirigira si la
    // respuesta confirma que las credenciales son correctas.
    window.location.href = "dashboard.html";
});
