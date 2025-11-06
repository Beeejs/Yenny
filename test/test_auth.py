# test/test_auth.py
import uuid
import pytest
from presentation.app import create_app
from data.utils.createTables import createTables


# Crea un email aleatorio
def rand_email() -> str:
  return f"user_{uuid.uuid4().hex[:8]}@example.com"

# Creacion de db de prueba temporal para los tests 
@pytest.fixture()
def client(tmp_path):
  app = create_app()
  app.config["TESTING"] = True
  # DB de prueba en archivo temporal
  app.config["DB_PATH"] = str((tmp_path / "test.db").resolve())

  # Crear tablas antes de correr los tests
  with app.app_context():
    conn = app.get_db()
    createTables(conn)

  return app.test_client()

# Datos de prueba
@pytest.fixture()
def user_data():
  return {
    "nombre": "UsuarioPrueba",
    "email": rand_email(),
    "password": "123456",
  }

# Registra y devuelve los datos para reutilizar en login
@pytest.fixture()
def registered_user(client, user_data):
  resp = client.post("/api/register", json=user_data)
  assert resp.status_code == 200, resp.get_json()
  return user_data

# Test de registro exitoso
def test_register_success(client, user_data):
  resp = client.post("/api/register", json=user_data)
  assert resp.status_code == 200
  body = resp.get_json()
  assert body["status"] is True
  assert "Usuario registrado correctamente" in body["message"]

# Test de login exitoso
def test_login_success(client, registered_user):
  resp = client.post("/api/login", json={
    "email": registered_user["email"],
    "password": registered_user["password"],
  })
  assert resp.status_code == 200
  body = resp.get_json()
  assert body["status"] is True
  assert "Usuario logueado correctamente" in body["message"]

# Test de login fallido por credenciales incorrectas
def test_login_invalid_credentials(client, registered_user):
  resp = client.post("/api/login", json={
    "email": registered_user["email"],
    "password": "mala_clave",
  })
  assert resp.status_code == 401
  body = resp.get_json()
  assert body["status"] is False
  assert "incorrect" in body["message"].lower()  # admite “incorrectos/incorrecta…”

# Test de login fallido por usuario no registrado
def test_login_invalid_user(client):
  resp = client.post("/api/login", json={
    "email": rand_email(),  # no registrado
    "password": "123456",
  })
  assert resp.status_code == 401
  body = resp.get_json()
  assert body["status"] is False
  assert "no existe" in body["message"].lower()
