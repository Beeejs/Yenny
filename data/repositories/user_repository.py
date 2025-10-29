# data/repository/user_repository.py
from flask import current_app

class UserRepository:
  def __init__(self):
    self.db = current_app.get_db()

  def create(self, nombre: str, rol: str, password_hash: str):
    cursor = self.db.cursor()
    cursor.execute(
      "INSERT INTO usuario (nombre, rol, password) VALUES (?, ?, ?)",
      (nombre, rol, password_hash)
    )
    self.db.commit()
    return cursor.lastrowid
