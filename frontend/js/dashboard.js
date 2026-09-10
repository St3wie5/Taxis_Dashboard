const API_URL = "http://127.0.0.1:5000";

const statsRow = document.getElementById("stats-row");
const fleetGrid = document.getElementById("fleet-grid");
const driverPanel = document.getElementById("driver-panel");

function renderStats(carros) {
    const activos = carros.filter(c => c.estado === "activo").length;
    const fs = carros.filter(c => c.estado === "f/s").length;
    const baja = carros.filter(c => c.estado === "baja").length;

    statsRow.innerHTML = `
        <div class="stat-chip activo"><strong>${activos}</strong> Activos</div>
        <div class="stat-chip fs"><strong>${fs}</strong> F/S</div>
        <div class="stat-chip baja"><strong>${baja}</strong> Baja</div>
    `;
}

function renderFleet(carros) {
    fleetGrid.innerHTML = "";
    carros.forEach(carro => {
        const btn = document.createElement("button");
        btn.className = "car-btn " + carro.estado.replace("/", "");
        btn.textContent = carro.id;
        btn.addEventListener("click", () => {
            document.querySelectorAll(".car-btn").forEach(b => b.classList.remove("selected"));
            btn.classList.add("selected");
            mostrarInfoCarro(carro);
        });
        fleetGrid.appendChild(btn);
    });
}

function mostrarInfoCarro(carro) {
    // TODO: aqui vamos a llamar a la API para traer el chofer
    // asignado actualmente a este carro (usando el endpoint de
    // asignaciones) y sus datos, en vez de solo mostrar el carro.
    driverPanel.innerHTML = `
        <div class="driver-header">
            <div class="driver-avatar">?</div>
            <div>
                <p class="name">Pendiente de conectar con la API</p>
                <p class="meta">Carro ${carro.id} - ${carro.estado}</p>
            </div>
        </div>
    `;
}

fetch(API_URL + "/carros")
    .then(function(respuesta) {
        return respuesta.json();
    })
    .then(function(carros) {
        renderStats(carros);
        renderFleet(carros);
    });