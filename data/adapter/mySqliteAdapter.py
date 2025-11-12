import sqlite3
from sqlite3 import Error
import os

from data.utils.data_default import cargar_libros_default
from data.utils.createTables import createTables

class MySqliteAdapter:
  """ Hacemos esto para que al correr main.py se guarde en la carpeta database """
  DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "database", "yenny.db"))
  
  def __init__(self, db_path=None):
    self.db_path = db_path or MySqliteAdapter.DB_FILE
    # Crea la carpeta database si no existe
    os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

  def connect(self):
    """Devuelve una nueva conexión independiente."""
    try:
      conn = sqlite3.connect(self.db_path)
      conn.row_factory = sqlite3.Row
      conn.execute("PRAGMA foreign_keys = ON;")
      print(f"Adaptador conectado a '{self.db_path}'.")
      return conn
    except Error as e:
      print(f"Error al conectar a SQLite: {e}")
      return None

  def setup_database(self):
    """Crea las tablas (solo se usa en main.py o inicialización)."""
    conn = self.connect()
    if conn:
      createTables(conn)
      cargar_libros_default(conn)
      conn.close()
      print("Tablas creadas correctamente.")

    else:
      print("No se pudo configurar la base de datos.")
