from flask import Blueprint, render_template, request, flash, redirect, url_for
from domain.managers.book_manager import BookManager

web_book_bp = Blueprint("web_book", __name__)

@web_book_bp.get("/libros")
def list_books():
  book_manager = BookManager()
  ok, books, message = book_manager.get_all()

  return render_template("books/list.html", books=books)

@web_book_bp.get("/books/<int:book_id>")
def view_book(book_id):
  book_manager = BookManager()
  ok, book, message = book_manager.get_one(book_id)

  if not ok or not book:
    flash(message or "No se pudo encontrar el libro", "danger")
    return redirect(url_for("web_book.list_books"))

  return render_template("books/view.html", book=book)

@web_book_bp.route("/books/new", methods=["GET", "POST"])
def new_book():
  if request.method == "POST":
    try:
      data = {
        "titulo": request.form["titulo"],
        "autor": request.form["autor"],
        "editorial": request.form["editorial"],
        "anio": int(request.form["anio"]),
        "precio": float(request.form["precio"]),
        "stock": int(request.form["stock"]),
      }
    except ValueError:
      flash("Por favor ingresa valores numéricos válidos para año, precio y stock", "danger")
      return render_template("books/new.html")

    book_manager = BookManager()
    ok, _, message = book_manager.create(data)
    if ok:
      flash("Libro creado con éxito", "success")
      return redirect(url_for("web_book.list_books"))
    else:
      flash(message or "Error al crear el libro", "danger")
  return render_template("books/new.html")


@web_book_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
  book_manager = BookManager()
  ok, book, message = book_manager.get_one(book_id)
  
  if not ok or not book:
    flash(message or "No se pudo encontrar el libro", "danger")
    return redirect(url_for("web_book.list_books"))
  
  if request.method == "POST":
    try:
      data = {
        "titulo": request.form["titulo"],
        "autor": request.form["autor"],
        "editorial": request.form["editorial"],
        "anio": int(request.form["anio"]),
        "precio": float(request.form["precio"]),
        "stock": int(request.form["stock"]),
      }
    except ValueError:
      flash("Por favor ingresa valores válidos para año, precio y stock", "danger")
      return render_template("books/view.html", book=book)
    
    success, _, msg = book_manager.update(book_id, data)
    if success:
      flash("Libro actualizado con éxito", "success")
      return redirect(url_for("web_book.list_books"))
    else:
      flash(msg or "Error al actualizar el libro", "danger")
  
  return render_template("books/view.html", book=book)

@web_book_bp.get("/books/<int:book_id>/delete")
def delete_book (book_id):
  book_manager = BookManager()
  ok, deleted_id, message = book_manager.delete(book_id)
  if ok:
        flash(f"Libro (ID {deleted_id}) eliminado correctamente.", "success")
  else:
        flash(message or "No se pudo eliminar el libro.", "danger")

  return redirect(url_for("web_book.list_books"))


