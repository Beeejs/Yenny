from flask import current_app
from typing import Dict, List, Any, Optional

class BookRepository:
  
  def __init__(self):
    self.db = current_app.get_db()


  def get_all(self) -> List[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_libro, titulo, editorial, anio, autor, precio, stock FROM libro"
    )

    books = cursor.fetchall()

    list_books = []

    for row in books:
      book_dict = {
        "id_libro": row[0],
        "titulo": row[1],
        "editorial": row[2],
        "anio": row[3],
        "autor": row[4],
        "precio": row[5],
        "stock": row[6]
      }
      list_books.append(book_dict)
      
    return list_books


  def get_one(self, book_id: int) -> Optional[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_libro, titulo, editorial, autor, precio, stock FROM libro WHERE id_libro = ?",
      (book_id,)
    )

    book = cursor.fetchone()

    if book:
      return {
        "id_libro": book[0],
        "titulo": book[1],
        "editorial": book[2],
        "autor": book[3],
        "precio": book[4],
        "stock": book[5]
      }
    return None


  def create(self, data: Dict[str, Any]) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "INSERT INTO libro (titulo, editorial, anio, autor, precio, stock) VALUES (?, ?, ?, ?, ?, ?)",
      (
        data.get("titulo"),
        data.get("editorial"),
        data.get("anio"),
        data.get("autor"),
        data.get("precio"),
        data.get("stock")
      )
    )
    self.db.commit()
    return cursor.lastrowid


  def update(self, book_id: int, data: Dict[str, Any]) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "UPDATE libro SET titulo = ?, editorial = ?, autor = ?, precio = ?, stock = ? WHERE id_libro = ?",
      (
        data.get("titulo"),
        data.get("editorial"),
        data.get("autor"),
        data.get("precio"),
        data.get("stock"),
        book_id
      )
    )
    self.db.commit()
    return cursor.rowcount


  def delete(self, book_id: int) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "DELETE FROM libro WHERE id_libro = ?", 
      (book_id,)
    )
    self.db.commit()
    return cursor.rowcount
  

  def set_categories(self, book_id: int, cat_ids: List[int]) -> None:
    cur = self.db.cursor()
    # Reemplazo total: borro y creo (transacción externa)
    cur.execute("DELETE FROM libro_categoria WHERE id_libro=?", (book_id,))
    if cat_ids:
      cur.executemany(
        "INSERT OR IGNORE INTO libro_categoria (id_libro, id_categoria) VALUES (?, ?)",
        [(book_id, cid) for cid in cat_ids]
      )
