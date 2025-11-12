from functools import wraps
from flask import session, jsonify

def require_auth(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    if "user_id" not in session:
      return jsonify({
        "status": False,
        "message": "No autenticado o sesión expirada."
      }), 401
    return fn(*args, **kwargs)
  return wrapper
