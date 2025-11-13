from flask import Blueprint, render_template, request, flash, redirect, url_for
from domain.managers.book_manager import BookManager
from domain.managers.category_manager import CategoryManager
from presentation.middlewares.web.login_required import login_required

web_book_bp = Blueprint("web_book", __name__)

@web_book_bp.get("/libros")
@login_required
def list_books():
  book_manager = BookManager()
  categroy_manager = CategoryManager()

  ok_cat, categories, msg_cat = categroy_manager.get_all()
  ok, books, message = book_manager.get_all()

  return render_template("books/list.html", books=books)

@web_book_bp.get("/books/<int:book_id>")
@login_required
def view_book(book_id):
  book_manager = BookManager()
  category_manager = CategoryManager()

  ok, book, message = book_manager.get_one(book_id)
  if not ok or not book:
    flash(message or "No se pudo encontrar el libro", "danger")
    return redirect(url_for("web_book.list_books"))

  ok_cat, categories, msg_cat = category_manager.get_all()
  if not ok_cat:
    flash(msg_cat or "No se pudieron cargar las categorías", "danger")
    categories = []

  return render_template("books/view.html", book=book, categories=categories)

@web_book_bp.route("/books/new", methods=["GET", "POST"])
@login_required
def new_book():
  book_manager = BookManager()
  categroy_manager = CategoryManager()

  ok_cat, categories, msg_cat = categroy_manager.get_all()
  
  if request.method == "POST":
    try:
      data = {
        "titulo": request.form["titulo"],
        "autor": request.form["autor"],
        "editorial": request.form["editorial"],
        "anio": int(request.form["anio"]),
        "precio": float(request.form["precio"]),
        "stock": int(request.form["stock"]),
        "categorias": [int(cid) for cid in request.form.getlist("categorias")]
      }
    except ValueError:
      flash("Por favor ingresa valores válidos para año, precio, stock y categorías", "danger")
      return render_template("books/new.html", categories=categories)

    ok, _, message = book_manager.create(data)
    if ok:
      flash("Libro creado con éxito", "success")
      return redirect(url_for("web_book.list_books"))
    else:
      flash(message or "Error al crear el libro", "danger")

  return render_template("books/new.html", categories=categories)



@web_book_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
  book_manager = BookManager()
  category_manager = CategoryManager()

  # Traer libro
  ok, book, message = book_manager.get_one(book_id)
  if not ok or not book:
    flash(message or "No se pudo encontrar el libro", "danger")
    return redirect(url_for("web_book.list_books"))

  # Traer todas las categorías para el select
  ok_cat, categories, msg_cat = category_manager.get_all()
  if not ok_cat:
    flash(msg_cat or "No se pudieron cargar las categorías", "danger")
    categories = []

  if request.method == "POST":
      try:
        data = {
          "titulo": request.form["titulo"],
          "autor": request.form["autor"],
          "editorial": request.form["editorial"],
          "anio": int(request.form["anio"]),
          "precio": float(request.form["precio"]),
          "stock": int(request.form["stock"]),
          "categorias": [int(cid) for cid in request.form.getlist("categorias")]
        }
      except ValueError:
        flash("Por favor ingresa valores válidos para año, precio, stock y categorías", "danger")
        return render_template("books/view.html", book=book, categories=categories)

      success, _, msg = book_manager.update(book_id, data)
      if success:
        flash("Libro actualizado con éxito", "success")
        return redirect(url_for("web_book.list_books"))
      else:
        flash(msg or "Error al actualizar el libro", "danger")

  return render_template("books/view.html", book=book, categories=categories)


@web_book_bp.get("/books/<int:book_id>/delete")
@login_required
def delete_book (book_id):
  book_manager = BookManager()
  ok, deleted_id, message = book_manager.delete(book_id)
  if ok:
    flash(f"Libro (ID {deleted_id}) eliminado correctamente.", "success")
  else:
    flash(message or "No se pudo eliminar el libro.", "danger")

  return redirect(url_for("web_book.list_books"))


