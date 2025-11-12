# presentation/middlewares/web/login_required.py
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    if not session.get("user_id"):
      flash("Debés iniciar sesión.", "warning")
      return redirect(url_for("web_auth.login"))
    return fn(*args, **kwargs)
  return wrapper
