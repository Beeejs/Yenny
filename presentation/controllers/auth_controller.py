# presentation/controllers/auth_controller.py
from flask import jsonify
from domain.managers.auth_manager import AuthManager

# Todo: se puede mejorar la parte del if not ok mandando solo un json y manejando lo que pasa el manager

def register(data: dict):
  auth_manager = AuthManager()

  ok, user, message = auth_manager.register(data)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Usuario registrado correctamente",
      "response": user
    }
  ), 200


def login(data: dict):
  auth_manager = AuthManager()

  ok, user, message = auth_manager.login(data)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or "Algo salio mal"
      }
    ), 401

  return jsonify(
    {
      "status": True,
      "message": "Usuario logueado correctamente",
      "response": user
    }
  ), 200


def logout():
  auth_manager = AuthManager()

  ok, response, message = auth_manager.logout()

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or "Algo salio mal"
      }
    ), 401

  return jsonify(
    {
      "status": True,
      "message": "Usuario logueado correctamente",
      "response": response
    }
  ), 200