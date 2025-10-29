# presentation/controllers/auth_controller.py
from flask import jsonify
from domain.managers.auth_manager import AuthManager


def register(data: dict):
  auth_manager = AuthManager()
  
  nombre = (data.get("nombre") or "").strip()
  rol = (data.get("rol") or "").strip()
  password = data.get("password") or ""

  ok, user = auth_manager.register(nombre, rol, password)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": user
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Usuario registrado correctamente",
      "response": user
    }
  ), 200
