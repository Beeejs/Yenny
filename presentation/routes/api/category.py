# presentation/routes/category.py
from flask import Blueprint, request
# controller
from ...controllers import category_controller
# middlewares
from ...middlewares.api.require_auth import require_auth
from ...middlewares.api.require_roles import require_roles

# Creamos el Blueprint
category_bp = Blueprint("category", __name__)

# Ruta: POST /api/category
@category_bp.route("/getAll", methods=["GET"])
@require_auth
@require_roles(["GERENTE", "EMPLEADO"])
def bookList():
  return category_controller.get_all()

@category_bp.route("/getOne/<int:category_id>", methods=["GET"])
@require_auth
@require_roles(["GERENTE", "EMPLEADO"])
def book(category_id):
  return category_controller.get_one(category_id)

@category_bp.route("/create", methods=["POST"])
@require_auth
@require_roles(["GERENTE"])
def create_book():
  data = request.get_json(silent=True) or {}
  return category_controller.create(data)

@category_bp.route("/update/<int:category_id>", methods=["PUT"])
@require_auth
@require_roles(["GERENTE"])
def update_book(category_id):
  data = request.get_json(silent=True) or {}
  return category_controller.update(category_id, data)

@category_bp.route("/delete/<int:category_id>", methods=["DELETE"])
@require_auth
@require_roles(["GERENTE"])
def delete_book(category_id):
  return category_controller.delete(category_id)

