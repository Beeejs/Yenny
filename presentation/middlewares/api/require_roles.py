from functools import wraps
from flask import session, jsonify

def require_roles(roles):
  """
  Permite siempre al ADMIN, y si no lo es,
  valida que el rol esté en la lista 'roles' pasada.
  """
  def decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      user_role = session.get("rol")
      if not user_role:
        return jsonify({"status": False, "message": "No autenticado"}), 401

      # si es admin, pasa directo
      if user_role == "ADMIN":
        return fn(*args, **kwargs)

      # si no es admin, validar los roles permitidos
      if user_role not in roles:
        return jsonify({"status": False, "message": "No autorizado"}), 403

      return fn(*args, **kwargs)
    return wrapper
  return decorator