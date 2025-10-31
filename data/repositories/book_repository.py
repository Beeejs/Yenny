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


  def get_one(self, id_libro: int) -> Optional[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_libro, titulo, editorial, autor, precio, stock FROM libro WHERE id_libro = ?",
      (id_libro,)
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
      "INSERT INTO libro (titulo, editorial, autor, precio, stock) VALUES (?, ?, ?, ?, ?)",
      (
        data.get("titulo"),
        data.get("editorial"),
        data.get("autor"),
        data.get("precio"),
        data.get("stock")
      )
    )
    self.db.commit()
    return cursor.lastrowid


  def update(self, id_libro: int, data: Dict[str, Any]) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "UPDATE libro SET titulo = ?, editorial = ?, autor = ?, precio = ?, stock = ? WHERE id_libro = ?",
      (
        data.get("titulo"),
        data.get("editorial"),
        data.get("autor"),
        data.get("precio"),
        data.get("stock"),
        id_libro
      )
    )
    self.db.commit()
    return cursor.rowcount


  def delete(self, id_libro: int) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "DELETE FROM libro WHERE id_libro = ?", 
      (id_libro,)
    )
    self.db.commit()
    return cursor.rowcount
