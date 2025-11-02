from flask import current_app
from typing import Dict, List, Any, Optional

class SaleRepository:
  
  def __init__(self):
    self.db = current_app.get_db()


  def get_all(self) -> List[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_venta, id_usuario, fecha, metodo_pago, estado FROM venta"
    )

    sales = cursor.fetchall()

    list_sales = []

    for row in sales:
      sale_dict = {
        "id_venta": row[0],
        "id_usuario": row[1],
        "fecha": row[2],
        "metodo_pago": row[3],
        "estado": row[4]
      }
      list_sales.append(sale_dict)
      
    return list_sales


  def get_one(self, sale_id: int) -> Optional[Dict[str, Any]]:
    cursor = self.db.cursor()
    cursor.execute(
      "SELECT id_venta, id_usuario, fecha, metodo_pago, estado FROM venta WHERE id_venta = ?",
      (sale_id,)
    )

    sale = cursor.fetchone()

    if sale:
      return {
        "id_venta": sale[0],
        "id_usuario": sale[1],
        "fecha": sale[2],
        "metodo_pago": sale[3],
        "estado": sale[4]
      }
    return None


  def create(self, data: Dict[str, Any]) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "INSERT INTO venta (id_usuario, fecha, metodo_pago, estado) VALUES (?, ?, ?, ?)",
      (
        data["id_usuario"],
        data["fecha"],
        data["metodo_pago"],
        data["estado"]
      )
    )
    self.db.commit()
    return cursor.lastrowid
  
  def insert_detalles(self, sale_id: int, detalles: List[Dict[str, Any]]) -> None:
    cur = self.db.cursor()
    cur.executemany(
      """INSERT INTO venta_detalle (id_libro, id_venta, cantidad, precio_unitario, subtotal)
         VALUES (?, ?, ?, ?, ?)""",
      [
        (d["id_libro"], sale_id, d["cantidad"], float(d["precio_unitario"]), float(d["subtotal"]))
        for d in detalles
      ]
    )


  def delete(self, sale_id: int) -> int:
    cursor = self.db.cursor()
    cursor.execute(
      "DELETE FROM venta_detalle WHERE id_venta = ?",
      (sale_id,)
    )
    cursor.execute(
      "DELETE FROM venta WHERE id_venta = ?", 
      (sale_id,)
    )
    self.db.commit()
    return cursor.rowcount
