import io


def test_crear_asignacion_cierra_la_anterior(client, mock_db, headers_admin):
    """Verifica la regla de negocio: al crear una asignacion nueva,
    primero se ejecuta el UPDATE que cierra la asignacion activa anterior
    del mismo chofer, y despues el INSERT de la nueva."""
    mock_db.fetchone.return_value = {"id": 10}

    respuesta = client.post("/asignaciones", json={
        "chofer_id": 1, "carro_id": "ECO01", "fecha_inicio": "2026-10-01",
    }, headers=headers_admin)

    assert respuesta.status_code == 201

    llamadas = mock_db.execute.call_args_list
    assert len(llamadas) == 2
    assert "UPDATE asignaciones" in llamadas[0][0][0]
    assert "INSERT INTO asignaciones" in llamadas[1][0][0]


def test_crear_asignacion_rechazada_para_chofer(client, mock_db, headers_chofer):
    respuesta = client.post("/asignaciones", json={
        "chofer_id": 1, "carro_id": "ECO01", "fecha_inicio": "2026-10-01",
    }, headers=headers_chofer)
    assert respuesta.status_code == 403


def test_chofer_actual_de_un_carro(client, mock_db, headers_admin):
    mock_db.fetchone.return_value = {"id": 1, "nombre": "Juan", "telefono": "8112223344"}

    respuesta = client.get("/carros/ECO01/chofer-actual", headers=headers_admin)

    assert respuesta.status_code == 200
    assert respuesta.get_json()["nombre"] == "Juan"


def test_chofer_actual_carro_sin_asignar(client, mock_db, headers_admin):
    mock_db.fetchone.return_value = None

    respuesta = client.get("/carros/ECO02/chofer-actual", headers=headers_admin)

    assert respuesta.status_code == 200
    assert respuesta.get_json() is None


def test_documentos_de_un_chofer(client, mock_db, headers_admin):
    mock_db.fetchall.return_value = [{"id": 1, "tipo_documento": "Licencia"}]

    respuesta = client.get("/choferes/1/documentos", headers=headers_admin)

    assert respuesta.status_code == 200
    assert len(respuesta.get_json()) == 1


def test_subir_documento_exitoso(client, mock_db, headers_admin):
    mock_db.fetchone.return_value = {"id": 7}

    datos_formulario = {
        "chofer_id": "1",
        "tipo_documento": "Licencia de conducir",
        "archivo": (io.BytesIO(b"contenido falso de pdf"), "licencia.pdf"),
    }

    respuesta = client.post(
        "/documentos/upload",
        data=datos_formulario,
        headers=headers_admin,
        content_type="multipart/form-data",
    )

    assert respuesta.status_code == 201
    assert respuesta.get_json()["id"] == 7


def test_subir_documento_sin_archivo(client, mock_db, headers_admin):
    respuesta = client.post(
        "/documentos/upload",
        data={"chofer_id": "1", "tipo_documento": "Licencia"},
        headers=headers_admin,
        content_type="multipart/form-data",
    )
    assert respuesta.status_code == 400


def test_subir_documento_requiere_admin(client, mock_db, headers_chofer):
    datos_formulario = {
        "chofer_id": "1",
        "tipo_documento": "Licencia",
        "archivo": (io.BytesIO(b"contenido falso"), "licencia.pdf"),
    }
    respuesta = client.post(
        "/documentos/upload",
        data=datos_formulario,
        headers=headers_chofer,
        content_type="multipart/form-data",
    )
    assert respuesta.status_code == 403
