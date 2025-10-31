# data/repository/user_repository.py
from flask import current_app

class UserRepository:
  def __init__(self):
    self.db = current_app.get_db()

  def create(self, data: dict):
    cursor = self.db.cursor()
    cursor.execute(
      "INSERT INTO usuario (nombre, email, rol, password) VALUES (?, ?, ?, ?)",
      (
        data.get("nombre"),
        data.get("email"),
        data.get("rol"),
        data.get("password")
      )
    )
    self.db.commit()
    return cursor.lastrowid


  def get_user_by_email(self, email: str) -> dict | None:
    cursor = self.db.cursor()
    
    cursor.execute(
      "SELECT id_usuario, nombre, email, rol, password FROM usuario WHERE email = ?", 
      (email,)
    )
    
    user_data = cursor.fetchone()
    
    if user_data:
      return {
        "id_usuario": user_data[0],
        "nombre": user_data[1],
        "email": user_data[2],
        "rol": user_data[3],
        "password": user_data[4] 
      }
    
    return None
  

  def update(self, id_usuario: int, data: dict):
    cursor = self.db.cursor()
    cursor.execute(
      "UPDATE usuario SET nombre = ?, email = ?, rol = ?, password = ? WHERE id_usuario = ?",
      (
        data.get("nombre"),
        data.get("email"),
        data.get("rol"),
        data.get("password"),
        id_usuario
      )
    )
    self.db.commit()
    return cursor.rowcount
  

  def delete(self, id_usuario: int):
    cursor = self.db.cursor()
    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
    self.db.commit()
    return cursor.rowcount