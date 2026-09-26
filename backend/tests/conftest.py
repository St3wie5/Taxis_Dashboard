import os
import sys

# Variables de entorno falsas para que app.py pueda importarse sin un .env real.
os.environ.setdefault("JWT_SECRET_KEY", "clave-secreta-solo-para-tests")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash

import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as cliente:
        yield cliente


@pytest.fixture
def mock_db(monkeypatch):
    """Reemplaza get_connection() por una base de datos falsa (mock),
    para que los tests no necesiten Postgres corriendo de verdad."""
    mock_cursor = MagicMock()
    mock_conexion = MagicMock()
    mock_conexion.cursor.return_value = mock_cursor
    monkeypatch.setattr(app_module, "get_connection", lambda: mock_conexion)
    return mock_cursor


@pytest.fixture
def hash_password_valido():
    return generate_password_hash("Sixat2026!")


@pytest.fixture
def token_admin():
    return app_module.generar_token({"id": 1, "username": "admin", "rol": "administrador"})


@pytest.fixture
def token_chofer():
    return app_module.generar_token({"id": 2, "username": "juan", "rol": "chofer"})


@pytest.fixture
def headers_admin(token_admin):
    return {"Authorization": "Bearer " + token_admin}


@pytest.fixture
def headers_chofer(token_chofer):
    return {"Authorization": "Bearer " + token_chofer}
