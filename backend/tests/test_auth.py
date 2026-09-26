import json


def test_login_exitoso(client, mock_db, hash_password_valido):
    mock_db.fetchone.return_value = {
        "id": 1, "username": "admin",
        "password_hash": hash_password_valido, "rol": "administrador",
    }

    respuesta = client.post("/login", json={"username": "admin", "password": "Sixat2026!"})

    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert "token" in datos
    assert datos["rol"] == "administrador"


def test_login_password_incorrecta(client, mock_db, hash_password_valido):
    mock_db.fetchone.return_value = {
        "id": 1, "username": "admin",
        "password_hash": hash_password_valido, "rol": "administrador",
    }

    respuesta = client.post("/login", json={"username": "admin", "password": "contrasena_mala"})

    assert respuesta.status_code == 401


def test_login_usuario_no_existe(client, mock_db):
    mock_db.fetchone.return_value = None

    respuesta = client.post("/login", json={"username": "fantasma", "password": "loquesea"})

    assert respuesta.status_code == 401


def test_login_sin_datos(client):
    respuesta = client.post("/login", json={})
    assert respuesta.status_code == 400


def test_endpoint_protegido_sin_token(client):
    respuesta = client.get("/choferes")
    assert respuesta.status_code == 401


def test_endpoint_protegido_token_invalido(client):
    respuesta = client.get("/choferes", headers={"Authorization": "Bearer token-inventado"})
    assert respuesta.status_code == 401


def test_endpoint_protegido_sin_prefijo_bearer(client, token_admin):
    respuesta = client.get("/choferes", headers={"Authorization": token_admin})
    assert respuesta.status_code == 401


def test_get_permitido_con_rol_chofer(client, mock_db, headers_chofer):
    mock_db.fetchall.return_value = []
    respuesta = client.get("/choferes", headers=headers_chofer)
    assert respuesta.status_code == 200


def test_post_rechazado_con_rol_chofer(client, mock_db, headers_chofer):
    respuesta = client.post("/choferes", json={"nombre": "Juan"}, headers=headers_chofer)
    assert respuesta.status_code == 403


def test_post_permitido_con_rol_administrador(client, mock_db, headers_admin):
    mock_db.fetchone.return_value = {"id": 5}
    respuesta = client.post("/choferes", json={
        "nombre": "Juan", "ap_paterno": "Perez", "ap_materno": "Lopez",
        "direccion": "Calle Falsa 123", "telefono": "8112223344",
        "fecha_inicio": "2026-01-01", "reportado": False,
    }, headers=headers_admin)
    assert respuesta.status_code == 201
