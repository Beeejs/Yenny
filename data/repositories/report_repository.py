from flask import current_app
from typing import Dict, List, Any


class ReportRepository:

  def __init__(self):
    self.db = current_app.get_db()

  def get_daily_sales_report(self, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    # Obtiene el reporte de ventas diarias
  
    cursor = self.db.cursor()

    query = """
            SELECT r.id_reporte, \
                    r.id_usuario, \
                    u.nombre as nombre_usuario, \
                    r.dia, \
                    r.ventas, \
                    r.unidades, \
                    r.monto
            FROM reporte_venta_diaria r
                      INNER JOIN usuario u ON r.id_usuario = u.id_usuario
            WHERE 1 = 1 \
            """

    params = []

    if start_date:
        query += " AND r.dia >= ?"
        params.append(start_date)

    if end_date:
        query += " AND r.dia <= ?"
        params.append(end_date)

    query += " ORDER BY r.dia DESC, u.nombre ASC"

    cursor.execute(query, params)
    reports = cursor.fetchall()

    list_reports = []
    for row in reports:
      report_dict = {
        "id_reporte": row[0],
        "id_usuario": row[1],
        "nombre_usuario": row[2],
        "dia": row[3],
        "ventas": row[4],
        "unidades": row[5],
        "monto": row[6]
      }
      list_reports.append(report_dict)

    return list_reports
  
  def get_book_popularity_report(self, start_date: str = None, end_date: str = None, limit: int = None) -> List[Dict[str, Any]]:

    # Obtiene el reporte de popularidad de libros
    
    cursor = self.db.cursor()

    query = """
        SELECT p.id_popularidad,
            p.id_libro,
            l.titulo,
            l.autor,
            l.editorial,
            p.dia,
            p.unidades,
            p.ingresos
        FROM popularidad_libro_diaria p
          INNER JOIN libro l ON p.id_libro = l.id_libro
        WHERE 1 = 1
        """

    params = []

    if start_date:
      query += " AND p.dia >= ?"
      params.append(start_date)

    if end_date:
      query += " AND p.dia <= ?"
      params.append(end_date)

    query += " ORDER BY p.dia DESC, p.unidades DESC, p.ingresos DESC"

    if limit:
      query += " LIMIT ?"
      params.append(limit)

    cursor.execute(query, params)
    reports = cursor.fetchall()

    list_reports = []
    for row in reports:
      book_id = row[1]

      # Obtener categorías del libro
      cursor.execute(
        "SELECT c.id_categoria, c.nombre FROM categoria c "
        "JOIN libro_categoria lc ON lc.id_categoria = c.id_categoria "
        "WHERE lc.id_libro = ?",
        (book_id,)
      )
      categories = [{"id_categoria": cat[0], "nombre": cat[1]} for cat in cursor.fetchall()]

      report_dict = {
        "id_popularidad": row[0],
        "id_libro": book_id,
        "titulo": row[2],
        "autor": row[3],
        "editorial": row[4],
        "dia": row[5],
        "unidades": row[6],
        "ingresos": row[7],
        "categorias": categories
      }
      list_reports.append(report_dict)

    return list_reports