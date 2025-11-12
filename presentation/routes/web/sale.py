from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from data.repositories.sale_repository import SaleRepository

web_sale_bp = Blueprint("web_sale", __name__)

# LISTAR
@web_sale_bp.get("/sales")
def list_sales():
    repo = SaleRepository()
    try:
        sales = repo.get_all()
        return render_template("sales/list.html", sales=sales)
    except Exception as e:
        current_app.logger.exception(e)
        flash("No se pudieron obtener las ventas.", "danger")
        return render_template("sales/list.html", sales=[])

# VER
@web_sale_bp.get("/sales/<int:sale_id>")
def view_sale(sale_id):
    repo = SaleRepository()
    try:
        sale = repo.get_one(sale_id)
        if not sale:
            flash("Venta no encontrada.", "danger")
            return redirect(url_for("web_sale.list_sales"))
        return render_template("sales/view.html", sale=sale)
    except Exception as e:
        current_app.logger.exception(e)
        flash("Ocurrió un error al cargar la venta.", "danger")
        return redirect(url_for("web_sale.list_sales"))

# NUEVO
@web_sale_bp.route("/sales/new", methods=["GET", "POST"])
def new_sale():
    if request.method == "POST":
        try:
            id_usuario   = int(request.form["id_usuario"])
            fecha_raw    = request.form["fecha"]  # viene como 'YYYY-MM-DDTHH:MM' del input datetime-local
            fecha        = fecha_raw.replace("T", " ")
            metodo_pago  = request.form["metodo_pago"]
            estado       = request.form["estado"]

            # Inserción simple de la venta (sin items todavía)
            repo = SaleRepository()
            new_id = repo.create({
                "id_usuario": id_usuario,
                "fecha": fecha,
                "metodo_pago": metodo_pago,
                "estado": estado
            })

            flash(f"Venta creada con éxito (ID {new_id}).", "success")
            return redirect(url_for("web_sale.list_sales"))
        except ValueError:
            flash("Por favor ingresa valores válidos (ID Usuario numérico, fecha válida).", "danger")
        except Exception as e:
            current_app.logger.exception(e)
            flash("Error al crear la venta.", "danger")

    return render_template("sales/new.html")

# EDITAR
@web_sale_bp.route("/sales/<int:sale_id>/edit", methods=["GET", "POST"])
def edit_sale(sale_id):
    repo = SaleRepository()

    # Cargar venta para mostrar/validar
    sale = repo.get_one(sale_id)
    if not sale:
        flash("Venta no encontrada.", "danger")
        return redirect(url_for("web_sale.list_sales"))

    if request.method == "POST":
        try:
            id_usuario   = int(request.form["id_usuario"])
            fecha_raw    = request.form["fecha"]
            fecha        = fecha_raw.replace("T", " ")
            metodo_pago  = request.form["metodo_pago"]
            estado       = request.form["estado"]

            # No hay método update en SaleRepository, actualizamos directo con la DB de la app
            db = current_app.get_db()
            cur = db.cursor()
            cur.execute(
                """
                UPDATE venta
                SET id_usuario = ?, fecha = ?, metodo_pago = ?, estado = ?
                WHERE id_venta = ?
                """,
                (id_usuario, fecha, metodo_pago, estado, sale_id)
            )
            db.commit()

            flash("Venta actualizada con éxito.", "success")
            return redirect(url_for("web_sale.list_sales"))
        except ValueError:
            flash("Por favor ingresa valores válidos (ID Usuario numérico, fecha válida).", "danger")
        except Exception as e:
            current_app.logger.exception(e)
            flash("Error al actualizar la venta.", "danger")

    # Render de edición (convertimos fecha 'YYYY-MM-DD HH:MM:SS' -> 'YYYY-MM-DDTHH:MM' para el input)
    fecha_val = sale["fecha"].replace(" ", "T") if sale.get("fecha") else ""
    sale_view = dict(sale)
    sale_view["fecha"] = fecha_val
    return render_template("sales/view.html", sale=sale_view)

# ELIMINAR
@web_sale_bp.get("/sales/<int:sale_id>/delete")
def delete_sale(sale_id):
    repo = SaleRepository()
    try:
        deleted_rows = repo.delete(sale_id)
        if deleted_rows == 0:
            flash("Venta no encontrada o ya eliminada.", "warning")
        else:
            flash(f"Venta (ID {sale_id}) eliminada correctamente.", "success")
    except Exception as e:
        current_app.logger.exception(e)
        flash("No se pudo eliminar la venta.", "danger")
    return redirect(url_for("web_sale.list_sales"))
