# presentation/controllers/book_controller.py
from flask import jsonify
from domain.managers.book_manager import BookManager

# TODO: VALIDAR QUE NO VENGAN CAMPOS NO PERMITIDOS (ver si se puede llegar a implementar)
def get_all():
  book_manager = BookManager()
  
  # Obtener libros
  ok, books, message = book_manager.get_all()

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
      "message": "Libros obtenidos correctamente",
      "response": books
    }
  ), 200


def get_one(id: int):
  book_manager = BookManager()
  
  # Obtener libro
  ok, book, message = book_manager.get_one(id)

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
      "message": "Libro obtenido correctamente",
      "response": book
    }
  ), 200

def create(data: dict):
  book_manager = BookManager()
  
  # Crear libro
  ok, book, message = book_manager.create(data)
  
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
      "message": "Libro creado correctamente",
      "response": book
    }
  ), 200


def update(id: int, data_update: dict):
  book_manager = BookManager()
  
  # Actualizar libro
  ok, book, message = book_manager.update(id, data_update)

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
      "message": "Libro actualizado correctamente",
      "response": book
    }
  ), 200


def delete(id: int):
  book_manager = BookManager()
  
  # Eliminar libro
  ok, book, message = book_manager.delete(id)

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
  
