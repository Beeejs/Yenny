# presentation/routes/book.py
from flask import Blueprint, request
# controller
from ...controllers import book_controller
# middlewares
from ...middlewares.api.require_auth import require_auth
from ...middlewares.api.require_roles import require_roles


# Creamos el Blueprint
book_bp = Blueprint("book", __name__)

# Ruta: POST /api/book
@book_bp.route("/getAll", methods=["GET"])
@require_auth
@require_roles(["GERENTE", "EMPLEADO"])
def bookList():
  return book_controller.get_all()

@book_bp.route("/getOne/<int:book_id>", methods=["GET"])
@require_auth
@require_roles(["GERENTE", "EMPLEADO"])
def book(book_id):
  return book_controller.get_one(book_id)

@book_bp.route("/create", methods=["POST"])
@require_roles(["GERENTE"])
@require_auth
def create_book():
  data = request.get_json(silent=True) or {}
  return book_controller.create(data)

@book_bp.route("/update/<int:book_id>", methods=["PUT"])
@require_auth
@require_roles(["GERENTE"])
def update_book(book_id):
  data = request.get_json(silent=True) or {}
  return book_controller.update(book_id, data)

@book_bp.route("/delete/<int:book_id>", methods=["DELETE"])
@require_auth
@require_roles(["GERENTE"])
def delete_book(book_id):
  return book_controller.delete(book_id)

