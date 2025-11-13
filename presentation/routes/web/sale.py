from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from domain.managers.sale_manager import SaleManager
from presentation.middlewares.web.login_required import login_required
from presentation.middlewares.web.require_roles import require_roles

web_sale_bp = Blueprint("web_sale", __name__)


# LISTAR
@web_sale_bp.get("/sales")
@login_required
def list_sales():
    sale_manager = SaleManager()
    try:
        ok, sales, message = sale_manager.get_all()
        return render_template("sales/list.html", sales=sales)
    except Exception as e:
        current_app.logger.exception(e)
        flash("No se pudieron obtener las ventas.", "danger")
        return render_template("sales/list.html", sales=[])


# VER
@web_sale_bp.get("/sales/<int:sale_id>")
@login_required
def view_sale(sale_id):
    sale_manager = SaleManager()
    try:
        ok, sale, message = sale_manager.get_one(sale_id)
        if not sale:
            flash("Venta no encontrada.", "danger")
            return redirect(url_for("web_sale.list_sales"))
        return render_template("sales/view.html", sale=sale, sale_items=sale.get("items", []))
    except Exception as e:
        current_app.logger.exception(e)
        flash("Ocurrió un error al cargar la venta.", "danger")
        return redirect(url_for("web_sale.list_sales"))


# NUEVO
@web_sale_bp.route("/sales/new", methods=["GET", "POST"])
@login_required
def new_sale():
    if request.method == "POST":
        try:
            id_usuario = session.get("user_id")
            if not id_usuario:
                flash("Debes estar logueado para crear una venta.", "danger")
                return redirect(url_for("web_auth.login"))

            fecha_raw = request.form["fecha"]
            fecha = fecha_raw.replace("T", " ") + ":00"
            metodo_pago = request.form["metodo_pago"]
            estado = request.form["estado"]

            # Reconstruir lista de items desde el formulario
            ids = request.form.getlist("id_libro[]")
            cantidades = request.form.getlist("cantidad[]")

            items = []
            for i in range(len(ids)):
                if ids[i] and cantidades[i]:
                    items.append({
                        "id_libro": int(ids[i]),
                        "cantidad": int(cantidades[i])
                    })

            # Validaciones
            if not metodo_pago or not estado:
                flash("Debe seleccionar método de pago y estado.", "danger")
                return render_template("sales/new.html")

            if len(items) == 0:
                flash("Debe agregar al menos un libro a la venta.", "danger")
                return render_template("sales/new.html")

            # Crear venta usando SaleManager
            sale_manager = SaleManager()
            ok, sale, message = sale_manager.create({
                "id_usuario": id_usuario,
                "fecha": fecha,
                "metodo_pago": metodo_pago,
                "estado": estado,
                "items": items
            })

            if not ok:
                flash(f"Error al crear la venta: {message}", "danger")
                return render_template("sales/new.html")

            flash("Venta creada con éxito.", "success")
            return redirect(url_for("web_sale.list_sales"))

        except Exception as e:
            current_app.logger.exception(e)
            flash(f"Error inesperado: {str(e)}", "danger")

    return render_template("sales/new.html")


# EDITAR
@web_sale_bp.route("/sales/<int:sale_id>/edit", methods=["GET", "POST"])
@login_required
def edit_sale(sale_id):
    sale_manager = SaleManager()

    ok, sale, message = sale_manager.get_one(sale_id)
    if not sale:
        flash("Venta no encontrada.", "danger")
        return redirect(url_for("web_sale.list_sales"))
    
    # Obtener el id_usuario de la sesión actual
    id_usuario = session.get("user_id")

    if not id_usuario:
        flash("Debes estar logueado para crear una venta.", "danger")
        return redirect(url_for("web_auth.login"))

    if request.method == "POST":
        try:
            fecha_raw = request.form["fecha"]
            fecha = fecha_raw.replace("T", " ")
            metodo_pago = request.form["metodo_pago"]
            estado = request.form["estado"]

            db = current_app.get_db()
            cur = db.cursor()
            cur.execute(
                """
                UPDATE venta
                SET id_usuario  = ?,
                    fecha       = ?,
                    metodo_pago = ?,
                    estado      = ?
                WHERE id_venta = ?
                """,
                (id_usuario, fecha, metodo_pago, estado, sale_id)
            )
            db.commit()

            flash("Venta actualizada con éxito.", "success")
            return redirect(url_for("web_sale.list_sales"))

        except ValueError:
            flash("Por favor ingresa valores válidos.", "danger")
        except Exception as e:
            current_app.logger.exception(e)
            flash("Error al actualizar la venta.", "danger")

    fecha_val = sale["fecha"].replace(" ", "T") if sale.get("fecha") else ""
    sale_view = dict(sale)
    sale_view["fecha"] = fecha_val
    return render_template("sales/view.html", sale=sale_view)


# ELIMINAR
@web_sale_bp.get("/sales/<int:sale_id>/delete")
@login_required
# solo esta parte el empleado comun no puede eliminar
@require_roles("ADMIN", "GERENTE")
def delete_sale(sale_id):
    sale_manager = SaleManager()
    try:
        ok, deleted_rows, message = sale_manager.delete(sale_id)
        if deleted_rows == 0:
            flash("Venta no encontrada o ya eliminada.", "warning")
        else:
            flash("Venta eliminada correctamente.", "success")
    except Exception as e:
        current_app.logger.exception(e)
        flash("No se pudo eliminar la venta.", "danger")
    return redirect(url_for("web_sale.list_sales"))
