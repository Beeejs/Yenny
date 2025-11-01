# presentation/controllers/book_controller.py
from flask import jsonify
from domain.managers.category_manager import CategoryManager

# TODO: VALIDAR QUE NO VENGAN CAMPOS NO PERMITIDOS (ver si se puede llegar a implementar)
def get_all():
  category_manager = CategoryManager()
  
  # Obtener categorias
  ok, categories, message = category_manager.get_all()

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
      "message": "Categorias obtenidas correctamente",
      "response": categories
    }
  ), 200


def get_one(id: int):
  category_manager = CategoryManager()
  
  # Obtener categoria
  ok, category, message = category_manager.get_one(id)

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
      "message": "Categoria obtenida correctamente",
      "response": category
    }
  ), 200

def create(data: dict):
  category_manager = CategoryManager()
  
  # Crear categoria
  ok, category, message = category_manager.create(data)
  
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
      "message": "Categoria creada correctamente",
      "response": category
    }
  ), 200


def update(id: int, data_update: dict):
  category_manager = CategoryManager()
  
  # Actualizar categoria
  ok, category, message = category_manager.update(id, data_update)

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
      "message": "Categoria actualizada correctamente",
      "response": category
    }
  ), 200


def delete(id: int):
  category_manager = CategoryManager()
  
  # Eliminar categoria
  ok, category, message = category_manager.delete(id)

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
      "message": "Libro eliminado correctamente"
    }
  ), 200
  
