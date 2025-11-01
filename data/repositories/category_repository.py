from flask import current_app
from typing import Dict, List, Any, Optional

class CategoryRepository:
  
  def __init__(self):
    self.db = current_app.get_db()


  def get_all(self) -> List[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_categoria, nombre, descripcion FROM categoria"
    )

    categories = cursor.fetchall()

    list_categories = []

    for row in categories:
      book_dict = {
        "id_categoria": row[0],
        "nombre": row[1],
        "descripcion": row[2]
      }
      list_categories.append(book_dict)
      
    return list_categories


  def get_one(self, category_id: int) -> Optional[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_categoria, nombre, descripcion FROM categoria WHERE id_categoria = ?",
      (category_id,)
    )

    category = cursor.fetchone()

    if category:
      return {
        "id_categoria": category[0],
        "nombre": category[1],
        "descripcion": category[2]
      }
    return None


  def create(self, data: Dict[str, Any]) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "INSERT INTO categoria (nombre, descripcion) VALUES (?, ?)",
      (
        data.get("nombre"),
        data.get("descripcion")
      )
    )
    self.db.commit()
    return cursor.lastrowid


  def update(self, category_id: int, data: Dict[str, Any]) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "UPDATE categoria SET nombre = ?, descripcion = ? WHERE id_categoria = ?",
      (
        data.get("nombre"),
        data.get("descripcion"),
        category_id
      )
    )
    self.db.commit()
    return cursor.rowcount


  def delete(self, category_id: int) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "DELETE FROM categoria WHERE id_categoria = ?", 
      (category_id,)
    )
    self.db.commit()
    return cursor.rowcount
  
  def categories_exist(self, cat_ids: List[int]) -> tuple[bool, list[int]]:
    if not cat_ids:
        return True, []
    cur = self.db.cursor()
    q = "SELECT id_categoria FROM categoria WHERE id_categoria IN ({})".format(
        ",".join("?" * len(cat_ids))
    )
    cur.execute(q, cat_ids)
    found = {row[0] for row in cur.fetchall()}
    missing = [cid for cid in cat_ids if cid not in found]
    return (len(missing) == 0), missing
