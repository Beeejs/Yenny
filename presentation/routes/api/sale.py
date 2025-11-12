# presentation/routes/sale.py
from flask import Blueprint, request
# controller
from ...controllers import sale_controller
# middlewares
from ...middlewares.api.require_auth import require_auth
from ...middlewares.api.require_roles import require_roles

# Creamos el Blueprint
sale_bp = Blueprint("sale", __name__)

# Ruta: POST /api/sale
@sale_bp.route("/getAll", methods=["GET"])
@require_auth
@require_roles(["STAFF"])
def saleList():
  return sale_controller.get_all()

@sale_bp.route("/getOne/<int:sale_id>", methods=["GET"])
@require_auth
@require_roles(["STAFF"])
def sale(sale_id):
  return sale_controller.get_one(sale_id)

@sale_bp.route("/create", methods=["POST"])
@require_auth
@require_roles(["STAFF"])
def create_sale():
  data = request.get_json(silent=True) or {}
  return sale_controller.create(data)

@sale_bp.route("/update/<int:sale_id>", methods=["PUT"])
@require_auth
def update_sale(sale_id):
  data = request.get_json(silent=True) or {}
  return sale_controller.update(sale_id, data)

@sale_bp.route("/delete/<int:sale_id>", methods=["DELETE"])
@require_auth
def delete_sale(sale_id):
  return sale_controller.delete(sale_id)

