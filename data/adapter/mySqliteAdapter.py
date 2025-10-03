import sqlite3
from sqlite3 import Error

from utils.createTables import createTables 

class MySqliteAdapter:
  DB_FILE = "yenny.db"
  
  def __init__(self):
    self.connection = None
    self.connect()

  def connect(self):
    """Método privado para establecer la conexión real."""
    try:
      self.connection = sqlite3.connect(MySqliteAdapter.DB_FILE)
      self.connection.row_factory = sqlite3.Row
      self.connection.execute("PRAGMA foreign_keys = ON;")
      print(f"Adaptador conectado a '{MySqliteAdapter.DB_FILE}'.")
    except Error as e:
      print(f"Error al conectar a SQLite: {e}")
      self.connection = None # Aseguramos que la conexión sea None si falla

  def setup_database(self):
    if self.connection:
      createTables(self.connection)
    else:
      print("No se puede configurar la DB: No hay conexión.")

  def get_connection(self):
    if self.connection is None:
      raise ConnectionError("La conexión a la base de datos no está activa.")
    return self.connection

  def close_connection(self):
    if self.connection:
      self.connection.close()
      print("Conexión a SQLite cerrada.")

# Bloque de ejecución: Ejecuta la CONFIGURACIÓN SOLO si se corre este archivo mediante consola
if __name__ == "__main__":
    adapter = None
    try:
      adapter = MySqliteAdapter()
      adapter.setup_database()
    except Exception as e:
        print(f"Error fatal durante la inicialización: {e}")
    finally:
      if adapter:
        adapter.close_connection()