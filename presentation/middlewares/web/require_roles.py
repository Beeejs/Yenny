# presentation/middlewares/web/require_roles.py
from functools import wraps
from flask import session, redirect, url_for, flash

def require_roles(*roles):
  def deco(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      if session.get("rol") not in roles:
        flash("No tenés permisos para realizar esta acción o ver esta sección.", "danger")
        return redirect(url_for("home"))
      return fn(*args, **kwargs)
    return wrapper
  return deco