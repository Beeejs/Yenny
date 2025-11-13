from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from domain.managers.auth_manager import AuthManager

web_auth_bp = Blueprint("web_auth", __name__)

# --- LOGIN ---
@web_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    auth_manager = AuthManager()

    if request.method == "POST":
        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        ok, user, message = auth_manager.login(data)

        if not ok:
            flash(message or "Error al iniciar sesión", "danger")
            return redirect(url_for("web_auth.login"))

        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for("home"))

    return render_template("auth/login.html")


# --- REGISTER ---
@web_auth_bp.route("/register", methods=["GET", "POST"])
def register():
    auth_manager = AuthManager()

    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        ok, user, message = auth_manager.register(data)

        if not ok:
            flash(message or "Error al registrarse", "danger")
            return redirect(url_for("web_auth.register"))

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("web_auth.login"))

    return render_template("auth/register.html")

@web_auth_bp.route("/logout")
def logout():
    auth_manager = AuthManager()
    ok, _, message = auth_manager.logout()
    if not ok:
        flash(message or "Error al cerrar sesión", "danger")
    else:
        flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("web_auth.login"))
