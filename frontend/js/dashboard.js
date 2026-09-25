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
    const url = API_URL + "/carros/" + carro.id + "/chofer-actual";

    driverPanel.innerHTML = `
        <p class="empty">Cargando información del chofer...</p>
    `;

    fetch(url)
    .then(function(respuesta) {
        if (!respuesta.ok) {
            throw new Error("No se pudo consultar el chofer");
        }
        return respuesta.json();
    })
    .then(function(chofer) {
        if (!chofer) {
            driverPanel.innerHTML = `
                <p class="empty">El carro ${carro.id} no tiene un chofer asignado.</p>
                <a class="btn-primary driver-edit-link" href="asignar.html?carro_id=${encodeURIComponent(carro.id)}">Asignar chofer</a>
            `;
            return;
        }

        const nombreCompleto = [
            chofer.nombre,
            chofer.ap_paterno,
            chofer.ap_materno
        ].filter(Boolean).join(" ");

        driverPanel.innerHTML = `
            <div class="driver-header">
                <div class="driver-avatar">${chofer.nombre?.charAt(0).toUpperCase() || "?"}</div>
                <div>
                    <p class="name">${nombreCompleto || "Chofer sin nombre"}</p>
                    <p class="meta">Carro ${carro.id} - ${carro.estado}</p>
                    <p class="meta">Teléfono: ${chofer.telefono || "No registrado"}</p>
                </div>
            </div>
            <a class="btn-primary driver-edit-link" href="agregar-chofer.html?id=${chofer.id}">Editar chofer</a>
        `;
    })
    .catch(function(error) {
        console.error(error);
        driverPanel.innerHTML = `
            <p class="empty">No se pudo cargar la información del chofer.</p>
        `;
    });
}

fetch(API_URL + "/carros")
    .then(function(respuesta) {
        return respuesta.json();
    })
    .then(function(carros) {
        renderStats(carros);
        renderFleet(carros);
    });