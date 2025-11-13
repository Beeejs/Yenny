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
    # Obtener la venta principal
    cursor.execute(
      "SELECT id_venta, id_usuario, fecha, metodo_pago, estado FROM venta WHERE id_venta = ?",
      (sale_id,)
    )
    sale = cursor.fetchone()

    if sale is None:
      return None

    # Obtener los detalles (items de la venta)
    cursor.execute("""
      SELECT 
        vd.id_libro,
        l.titulo,
        vd.cantidad,
        vd.precio_unitario,
        vd.subtotal
      FROM venta_detalle vd
      JOIN libro l ON vd.id_libro = l.id_libro
      WHERE vd.id_venta = ?
    """, (sale_id,))
    details = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    items = [dict(zip(columns, row)) for row in details]

    # Retornar todo junto
    return {
      "id_venta": sale[0],
      "id_usuario": sale[1],
      "fecha": sale[2],
      "metodo_pago": sale[3],
      "estado": sale[4],
      "items": items 
    }



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
    cur = self.db.cursor()

    cur.execute("""
      SELECT id_usuario, DATE (fecha)
      FROM venta
      WHERE id_venta = ?
      """, (sale_id,))
    venta_row = cur.fetchone()

    if not venta_row:
        return 0

    id_usuario = venta_row[0]
    dia = venta_row[1]

    cur.execute("""
      SELECT id_libro, cantidad, subtotal
      FROM venta_detalle
      WHERE id_venta = ?
      """, (sale_id,))
    detalles = cur.fetchall()

    total_unidades = 0
    total_monto = 0.0

    for det in detalles:
      id_libro = det[0]
      cantidad = det[1]
      subtotal = det[2]

      total_unidades += cantidad
      total_monto += subtotal

      # Revertir popularidad por libro
      cur.execute("""
        UPDATE popularidad_libro_diaria
        SET unidades = unidades - ?,
            ingresos = ingresos - ?
        WHERE id_libro = ?
          AND dia = ?
        """, (cantidad, subtotal, id_libro, dia))

      # Si queda en cero, borrar
      cur.execute("""
        DELETE
        FROM popularidad_libro_diaria
        WHERE id_libro = ?
          AND dia = ?
          AND unidades = 0
          AND ingresos = 0
        """, (id_libro, dia))

    # Revertir reporte diario
    cur.execute("""
      UPDATE reporte_venta_diaria
      SET ventas   = ventas - 1,
          unidades = unidades - ?,
          monto    = monto - ?
      WHERE id_usuario = ?
        AND dia = ?
      """, (total_unidades, total_monto, id_usuario, dia))

    # Si quedó todo en cero, eliminar fila del día
    cur.execute("""
      DELETE
      FROM reporte_venta_diaria
      WHERE id_usuario = ?
        AND dia = ?
        AND ventas = 0
        AND unidades = 0
        AND monto = 0
      """, (id_usuario, dia))

    # Eliminar detalles y venta
    cur.execute("DELETE FROM venta_detalle WHERE id_venta = ?", (sale_id,))
    cur.execute("DELETE FROM venta WHERE id_venta = ?", (sale_id,))

    self.db.commit()
    return cur.rowcount
  

  def upsert_reporte_diario(self, id_usuario: int, dia: str, ventas_delta: int, unidades_delta: int, monto_delta: float) -> None:
    cur = self.db.cursor()
    cur.execute(
      """
      INSERT INTO reporte_venta_diaria (id_usuario, dia, ventas, unidades, monto)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(id_usuario, dia) DO UPDATE SET
        ventas   = ventas   + excluded.ventas,
        unidades = unidades + excluded.unidades,
        monto    = monto    + excluded.monto
      """,
      (id_usuario, dia, ventas_delta, unidades_delta, monto_delta)
    )

  def upsert_popularidad_libro(self, id_libro: int, dia: str, unidades_delta: int, ingresos_delta: float) -> None:
    cur = self.db.cursor()
    cur.execute(
      """
      INSERT INTO popularidad_libro_diaria (id_libro, dia, unidades, ingresos)
      VALUES (?, ?, ?, ?)
      ON CONFLICT(id_libro, dia) DO UPDATE SET
        unidades = unidades + excluded.unidades,
        ingresos = ingresos + excluded.ingresos
      """,
      (id_libro, dia, unidades_delta, ingresos_delta)
    )

