CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('administrador', 'chofer'))
);

INSERT INTO usuarios (username, password_hash, rol)
VALUES ('admin', 'scrypt:32768:8:1$QVkKncsUOL37Mg6e$48f26b52f6f2fba182220007562d303165f91df5bc4ff448683f5b52164273fb1154033dc4a3dd9880ae30908647b171e26703fcaaacf8015f5689c1f1a47012', 'administrador');
