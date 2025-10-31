# presentation/routes/auth.py
from flask import Blueprint, request
# controller
from ..controllers import book_controller

# Creamos el Blueprint
book_bp = Blueprint("book", __name__)

# Ruta: POST /api/book
@book_bp.route("/getAll", methods=["GET"])
def bookList():
  return book_controller.get_all()

@book_bp.route("/getOne/<int:book_id>", methods=["GET"])
def book(book_id):
  return book_controller.get_one(book_id)

@book_bp.route("/create", methods=["POST"])
def create_book():
  data = request.get_json(silent=True) or {}
  return book_controller.create(data)

@book_bp.route("/update/<int:book_id>", methods=["PUT"])
def update_book(book_id):
  data = request.get_json(silent=True) or {}
  return book_controller.update(book_id, data)

@book_bp.route("/delete/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
  return book_controller.delete(book_id)

