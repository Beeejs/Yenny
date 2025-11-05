# presentation/controllers/category_controller.py
from flask import jsonify
from domain.managers.user_manager import UserManager

def get_all():
  user_manager = UserManager()
  
  # Obtener usuarios
  ok, users, message = user_manager.get_all()

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
      "message": "Usuarios obtenidos correctamente",
      "response": users
    }
  ), 200


def get_one(id: int):
  user_manager = UserManager()
  
  # Obtener usuario
  ok, user, message = user_manager.get_one(id)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or  "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Usuarios obtenidos correctamente",
      "response": user
    }
  ), 200

def create(data: dict):
  user_manager = UserManager()
  
  # Crear usuario
  ok, user, message = user_manager.create(data)
  
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
      "message": "Usuario creado correctamente",
      "response": user
    }
  ), 200


def update(id: int, data_update: dict):
  user_manager = UserManager()
  
  # Actualizar usuario
  ok, user, message = user_manager.update(id, data_update)

  if not ok:
    return jsonify(
      {
        "status": False,
        "message": message or  "Algo salio mal",
      }
    ), 400

  return jsonify(
    {
      "status": True,
      "message": "Usuario actualizado correctamente",
      "response": user
    }
  ), 200


def delete(id: int):
  user_manager = UserManager()
  
  # Eliminar categoria
  ok, user, message = user_manager.delete(id)

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
      "message": "Usuario eliminado correctamente"
    }
  ), 200
  
