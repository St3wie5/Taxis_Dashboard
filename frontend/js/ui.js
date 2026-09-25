function mostrarMensaje(texto, tipo) {
    const contenedor = document.getElementById("toast-container");
    if (!contenedor) {
        alert(texto);
        return;
    }

    const toast = document.createElement("div");
    toast.className = "toast " + (tipo === "error" ? "toast-error" : "toast-ok");
    toast.textContent = texto;
    contenedor.appendChild(toast);

    setTimeout(function () {
        toast.classList.add("toast-hide");
        setTimeout(function () { toast.remove(); }, 300);
    }, 2200);
}
