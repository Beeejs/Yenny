from flask import Blueprint, render_template, request, flash, redirect, url_for
from domain.managers.category_manager import CategoryManager
from presentation.middlewares.web.login_required import login_required

web_category_bp = Blueprint("web_category", __name__)


@web_category_bp.get("/categorias")
@login_required
def list_categories():
    category_manager = CategoryManager()
    ok, categories, message = category_manager.get_all()

    if not ok:
        flash(message or "No se pudieron obtener las categorías.", "danger")
        return render_template("categories/list.html", categories=[])

    return render_template("categories/list.html", categories=categories)


@web_category_bp.get("/categories/<int:category_id>")
@login_required
def view_category(category_id):
    category_manager = CategoryManager()
    ok, category, message = category_manager.get_one(category_id)

    if not ok or not category:
        flash(message or "No se pudo encontrar la categoría", "danger")
        return redirect(url_for("web_category.list_categories"))

    return render_template("categories/view.html", category=category)


@web_category_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def new_category():
    if request.method == "POST":
        try:
            data = {
                "nombre": request.form["nombre"],
                "descripcion": request.form["descripcion"]
            }
        except KeyError as e:
            flash(f"Falta el campo: {str(e)}", "danger")
            return render_template("categories/new.html")

        category_manager = CategoryManager()
        ok, _, message = category_manager.create(data)

        if ok:
            flash("Categoría creada con éxito", "success")
            return redirect(url_for("web_category.list_categories"))
        else:
            flash(message or "Error al crear la categoría", "danger")

    return render_template("categories/new.html")


@web_category_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category_manager = CategoryManager()
    ok, category, message = category_manager.get_one(category_id)

    if not ok or not category:
        flash(message or "No se pudo encontrar la categoría", "danger")
        return redirect(url_for("web_category.list_categories"))

    if request.method == "POST":
        try:
            data = {
                "nombre": request.form["nombre"],
                "descripcion": request.form["descripcion"]
            }
        except KeyError as e:
            flash(f"Falta el campo: {str(e)}", "danger")
            return render_template("categories/view.html", category=category)

        success, _, msg = category_manager.update(category_id, data)
        if success:
            flash("Categoría actualizada con éxito", "success")
            return redirect(url_for("web_category.list_categories"))
        else:
            flash(msg or "Error al actualizar la categoría", "danger")

    return render_template("categories/view.html", category=category)


@web_category_bp.get("/categories/<int:category_id>/delete")
@login_required
def delete_category(category_id):
    category_manager = CategoryManager()
    ok, deleted_id, message = category_manager.delete(category_id)

    if ok:
        flash(f"Categoría (ID {deleted_id}) eliminada correctamente.", "success")
    else:
        flash(message or "No se pudo eliminar la categoría.", "danger")

    return redirect(url_for("web_category.list_categories"))