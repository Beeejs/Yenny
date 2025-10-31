# presentation/routes/auth.py
from flask import Blueprint, request
# controller
from ..controllers import auth_controller
from ..controllers import book_controller

# Creamos el Blueprint
auth_bp = Blueprint("auth", __name__)

# Ruta: POST /api/register
@auth_bp.route("/register", methods=["POST"])
def register():
  data = request.get_json(silent=True) or {}
  return auth_controller.register(data)

# Ruta: POST /api/login
@auth_bp.route("/login", methods=["POST"])
def login():
  data = request.get_json(silent=True) or {}
  return auth_controller.login(data)
