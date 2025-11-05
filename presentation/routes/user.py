# presentation/routes/user.py
from flask import Blueprint, request
# controller
from ..controllers import user_controller
# middlewares
from ..middlewares.require_auth import require_auth
from ..middlewares.require_roles import require_roles

# Creamos el Blueprint
user_bp = Blueprint("user", __name__)

# Ruta: POST /api/user
@user_bp.route("/getAll", methods=["GET"])
@require_auth
def bookList():
  return user_controller.get_all()

@user_bp.route("/getOne/<int:user_id>", methods=["GET"])
@require_auth
def book(user_id):
  return user_controller.get_one(user_id)

@user_bp.route("/create", methods=["POST"])
@require_auth
def create_book():
  data = request.get_json(silent=True) or {}
  return user_controller.create(data)

@user_bp.route("/update/<int:user_id>", methods=["PUT"])
@require_auth
def update_book(user_id):
  data = request.get_json(silent=True) or {}
  return user_controller.update(user_id, data)

@user_bp.route("/delete/<int:user_id>", methods=["DELETE"])
@require_auth
def delete_book(user_id):
  return user_controller.delete(user_id)

