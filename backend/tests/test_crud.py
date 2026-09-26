import pytest

# (endpoint base, id de ejemplo, payload valido para POST/PUT)
TABLAS = [
    ("/choferes", "1", {
        "nombre": "Juan", "ap_paterno": "Perez", "ap_materno": "Lopez",
        "direccion": "Calle Falsa 123", "telefono": "8112223344",
        "fecha_inicio": "2026-01-01", "reportado": False,
    }),
    ("/carros", "ECO01", {
        "id": "ECO01", "marca": "NISSAN", "modelo": "VERSA", "anio": 2024,
        "placas": "ABC123", "serie": "XYZ999", "motor": "MTR001",
        "duenio": "SIXAT", "estado": "activo",
    }),
    ("/citas_gob", "1", {
        "carro_id": "ECO01", "tipo_cita": "Verificacion",
        "fecha_cita": "2026-10-01", "estado": "pendiente",
    }),
    ("/mantenimientos", "1", {
        "carro_id": "ECO01", "tipo_mantenimiento": "Cambio de aceite",
        "fecha": "2026-10-01", "costo": 500, "kilometraje": 45000,
        "notas": "Rutina", "estado": "pendiente",
    }),
    ("/documentos", "1", {
        "chofer_id": 1, "tipo_documento": "Licencia",
        "archivo": "licencia.pdf", "fecha_subida": "2026-10-01",
    }),
]


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_get_lista_requiere_token(client, base, id_ejemplo, payload):
    respuesta = client.get(base)
    assert respuesta.status_code == 401


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_get_lista_con_token(client, mock_db, headers_admin, base, id_ejemplo, payload):
    mock_db.fetchall.return_value = []
    respuesta = client.get(base, headers=headers_admin)
    assert respuesta.status_code == 200
    assert respuesta.get_json() == []


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_post_requiere_rol_admin(client, mock_db, headers_chofer, base, id_ejemplo, payload):
    respuesta = client.post(base, json=payload, headers=headers_chofer)
    assert respuesta.status_code == 403


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_post_crea_registro_como_admin(client, mock_db, headers_admin, base, id_ejemplo, payload):
    mock_db.fetchone.return_value = {"id": id_ejemplo}
    respuesta = client.post(base, json=payload, headers=headers_admin)
    assert respuesta.status_code == 201


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_put_actualiza_como_admin(client, mock_db, headers_admin, base, id_ejemplo, payload):
    mock_db.rowcount = 1
    respuesta = client.put(base + "/" + id_ejemplo, json=payload, headers=headers_admin)
    assert respuesta.status_code == 200


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_delete_como_admin(client, mock_db, headers_admin, base, id_ejemplo, payload):
    respuesta = client.delete(base + "/" + id_ejemplo, headers=headers_admin)
    assert respuesta.status_code == 200


@pytest.mark.parametrize("base,id_ejemplo,payload", TABLAS)
def test_delete_rechazado_para_chofer(client, mock_db, headers_chofer, base, id_ejemplo, payload):
    respuesta = client.delete(base + "/" + id_ejemplo, headers=headers_chofer)
    assert respuesta.status_code == 403
